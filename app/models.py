from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

# SRS Input Model
class SRSInput(BaseModel):
    project_name: Optional[str] = Field(None, description="Project name")
    srs_version: Optional[str] = Field(None, description="Version of the SRS document")
    authors: Optional[str] = Field(None, description="Authors or contributors")
    creation_date: Optional[str] = Field(None, description="Date of creation")
    stakeholders: Optional[str] = Field(None, description="Stakeholders involved")
    expected_release_date: Optional[str] = Field(None, description="Expected delivery or release date")
    overview_summary: Optional[str] = Field(None, description="Brief summary of the system")
    main_purpose: Optional[str] = Field(None, description="Main purpose of the project")
    intended_users: Optional[str] = Field(None, description="Intended users or beneficiaries")
    srs_purpose: Optional[str] = Field(None, description="Purpose of this SRS document")
    scope: Optional[str] = Field(None, description="Scope of the software system")
    assumptions: Optional[str] = Field(None, description="Assumptions, dependencies, or constraints")
    acronyms: Optional[str] = Field(None, description="Acronyms, abbreviations, or references to explain")
    problem: Optional[str] = Field(None, description="Problem or challenge addressed")
    affected_parties: Optional[str] = Field(None, description="Who is affected and in what context")
    impacts: Optional[str] = Field(None, description="Impacts or inefficiencies caused by current state")
    resources: Optional[str] = Field(None, description="Resources and time allocated")
    constraints: Optional[str] = Field(None, description="Budgetary or technical constraints")
    mvp: Optional[str] = Field(None, description="Minimum viable solution")
    ideal_solution: Optional[str] = Field(None, description="Ideal solution if no constraints")
    deliverables: Optional[str] = Field(None, description="Expected deliverables of the system")
    delivery_stages: Optional[str] = Field(None, description="Important delivery stages or milestones")
    major_features: Optional[str] = Field(None, description="Major features or capabilities planned")
    datasheets: Optional[str] = Field(None, description="Technical specifications or datasheets")
    db_design: Optional[str] = Field(None, description="Main entities/tables and relationships")
    uiux: Optional[str] = Field(None, description="UI/UX design details")
    rabbit_holes: Optional[str] = Field(None, description="Feature ideas or areas for future exploration")
    out_of_scope: Optional[str] = Field(None, description="Explicitly out of scope items")
    restrictions: Optional[str] = Field(None, description="Technologies/methods/tools not to be used or legal/ethical restrictions")

# Database Models
class SRSSession(SQLModel, table=True):
    session_id: str = Field(primary_key=True)
    created_at: datetime
    updated_at: datetime
    project_name: str = Field(default="")
    srs_version: str = Field(default="1.0")
    authors: str = Field(default="")
    creation_date: str = Field(default="")
    stakeholders: str = Field(default="")
    expected_release_date: str = Field(default="")
    overview_summary: str = Field(default="")
    main_purpose: str = Field(default="")
    intended_users: str = Field(default="")
    srs_purpose: str = Field(default="")
    scope: str = Field(default="")
    assumptions: str = Field(default="")
    acronyms: str = Field(default="")
    problem: str = Field(default="")
    affected_parties: str = Field(default="")
    impacts: str = Field(default="")
    resources: str = Field(default="")
    constraints: str = Field(default="")
    mvp: str = Field(default="")
    ideal_solution: str = Field(default="")
    deliverables: str = Field(default="")
    delivery_stages: str = Field(default="")
    major_features: str = Field(default="")
    datasheets: str = Field(default="")
    db_design: str = Field(default="")
    uiux: str = Field(default="")
    rabbit_holes: str = Field(default="")
    out_of_scope: str = Field(default="")
    restrictions: str = Field(default="")
    history: str = Field(default="")
    status: str = Field(default="active")
    latest_proposal: Optional[str] = Field(default=None)

class SRSMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(foreign_key="srssession.session_id")
    role: str
    content: str
    reasoning: Optional[str] = None
    sequence: int = Field(index=True)
    timestamp: datetime

# Response Models
class SRSStartResponse(BaseModel):
    session_id: str
    question: str
    reason: str

class SRSContinueRequest(BaseModel):
    response: str

class SRSContinueResponse(BaseModel):
    question: str
    reason: str
    is_complete: bool = False

class SRSGenerateRequest(BaseModel):
    style: Optional[str] = None
    tone: Optional[str] = None

class SRSCustomPromptRequest(BaseModel):
    prompt: str