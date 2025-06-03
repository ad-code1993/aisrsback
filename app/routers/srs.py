from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
import uuid
from datetime import datetime
from ..database import get_session
from ..models import (
    SRSSession, SRSMessage, SRSInput,
    SRSStartResponse, SRSContinueRequest, 
    SRSContinueResponse, SRSGenerateRequest,
    SRSCustomPromptRequest
)
from ..agents import (
    srs_chat_agent, srs_structured_agent,
    srs_agent, SRS_BASE_PROMPT, format_srs_prompt, validate_response
)

router = APIRouter(prefix="/srs", tags=["SRS"])

@router.post("/start", response_model=SRSStartResponse)
async def start_srs_session(db: Session = Depends(get_session)):
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    session = SRSSession(session_id=session_id, created_at=now, updated_at=now)
    db.add(session)
    db.commit()  # Commit the session to ensure the session_id exists in the database
    try:
        ai_response = await srs_chat_agent.run(SRS_BASE_PROMPT.strip())
        if not ai_response or not hasattr(ai_response, "output"):
            raise HTTPException(status_code=500, detail="Failed to get initial AI response")
        db.add(SRSMessage(
            session_id=session_id,
            role="assistant",
            content=ai_response.output.question,
            reasoning=ai_response.output.reason,
            sequence=1,
            timestamp=now
        ))
        db.commit()
        return SRSStartResponse(
            session_id=session_id,
            question=ai_response.output.question,
            reason=ai_response.output.reason
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error starting session: {str(e)}")

@router.post("/{session_id}/continue", response_model=SRSContinueResponse)
async def continue_srs(session_id: str, request: SRSContinueRequest, db: Session = Depends(get_session)):
    session = db.get(SRSSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        messages = db.exec(
            select(SRSMessage).where(SRSMessage.session_id == session_id).order_by(SRSMessage.sequence)
        ).all()
        
        # Build conversation history
        history = SRS_BASE_PROMPT.strip() + "\n\n"
        for msg in messages:
            role = "Assistant" if msg.role == "assistant" else "User"
            history += f"{role}: {msg.content}\n"
        history += f"User: {request.response}\n"
        
        # Get and validate AI response
        raw_response = await srs_chat_agent.run(history)
        if not raw_response:
            raise HTTPException(status_code=500, detail="Empty AI response")
            
        try:
            ai_response = validate_response(raw_response.output)
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Failed to parse AI response: {str(e)}. Original response: {raw_response.output}"
            )
        
        # Determine if the session is complete
        is_complete = "all done" in ai_response.question.lower()
        
        # Save user and assistant messages to the database
        next_sequence = len(messages) + 1
        db.add(SRSMessage(
            session_id=session_id,
            role="user",
            content=request.response,
            sequence=next_sequence,
            timestamp=datetime.utcnow()
        ))
        db.add(SRSMessage(
            session_id=session_id,
            role="assistant",
            content=ai_response.question,
            reasoning=ai_response.reason,
            sequence=next_sequence + 1,
            timestamp=datetime.utcnow()
        ))
        
        # Finalize session if complete
        if is_complete:
            await finalize_srs(session, db, history)
        
        db.commit()
        return SRSContinueResponse(
            question=ai_response.question,
            reason=ai_response.reason,
            is_complete=is_complete
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error continuing session: {str(e)}"
        )

async def finalize_srs(session: SRSSession, db: Session, history: str):
    try:
        structured_result = await srs_structured_agent.run(history)
        if not structured_result or not hasattr(structured_result, "output"):
            raise Exception("Failed to generate structured SRS data")
        srs_data = structured_result.output.dict()
        for field in SRSInput.__fields__:
            if field in srs_data:
                setattr(session, field, srs_data[field])
        session.status = "complete"
        session.updated_at = datetime.utcnow()
        db.add(session)
    except Exception as e:
        raise Exception(f"Error finalizing SRS: {str(e)}")

@router.post("/{session_id}/generate")
async def generate_srs(session_id: str, request: SRSGenerateRequest, db: Session = Depends(get_session)):
    session = db.get(SRSSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    srs_data = SRSInput(**{field: getattr(session, field) for field in SRSInput.__fields__})
    extra = ""
    if request.style:
        extra += f"Style: {request.style}. "
    if request.tone:
        extra += f"Tone: {request.tone}."
    prompt = format_srs_prompt(srs_data) + extra
    try:
        result = await srs_agent.run(prompt)
        if not result or not hasattr(result, "output"):
            raise HTTPException(status_code=500, detail="Failed to generate SRS")
        session.latest_proposal = result.output
        session.updated_at = datetime.utcnow()
        db.add(session)
        db.commit()
        return {"srs": result.output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating SRS: {str(e)}")

@router.post("/{session_id}/custom")
async def custom_prompt_srs(session_id: str, request: SRSCustomPromptRequest, db: Session = Depends(get_session)):
    session = db.get(SRSSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    srs_data = SRSInput(**{field: getattr(session, field) for field in SRSInput.__fields__})
    prompt = format_srs_prompt(srs_data) + f"\n\nAdditional Instructions: {request.prompt}"
    try:
        result = await srs_agent.run(prompt)
        if not result or not hasattr(result, "output"):
            raise HTTPException(status_code=500, detail="Failed to generate SRS")
        return {"srs": result.output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating SRS: {str(e)}")

@router.get("/{session_id}")
def get_srs_session(session_id: str, db: Session = Depends(get_session)):
    session = db.get(SRSSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/{session_id}/latest")
def get_latest_srs(session_id: str, db: Session = Depends(get_session)):
    session = db.get(SRSSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.latest_proposal:
        raise HTTPException(status_code=404, detail="No generated SRS found")
    return {"srs": session.latest_proposal}
