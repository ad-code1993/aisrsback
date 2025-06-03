import asyncio
import json
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

class chat_output(BaseModel):
    reason: str = Field(..., description="Reasoning behind the question asked by the AI")
    question: str = Field(..., description="The question asked by the AI")


# SRS schema for SRS Q&A flow
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

SRS_BASE_PROMPT = """
You are a helpful assistant collecting information to build a complete software project proposal.

For each field below, ask the user a specific question. **For every question you ask, include a brief one-line reasoning** about why that information is important:

- project_name
- srs_version
- authors
- creation_date
- stakeholders
- expected_release_date
- overview_summary
- main_purpose
- intended_users
- srs_purpose
- scope
- assumptions
- acronyms
- problem
- affected_parties
- impacts
- resources
- constraints
- mvp
- ideal_solution
- deliverables
- delivery_stages
- major_features
- datasheets
- db_design
- uiux
- rabbit_holes
- out_of_scope
- restrictions

Do not generate a final proposal yet. Ask only one question at a time.
Format your message as:
"Reason: <reason>. \nQuestion: <your question here>"

If all fields are collected, say "All done" and stop asking.
"""



# SRS Agents
srs_chat_agent = Agent("groq:gemma2-9b-it", system_prompt=SRS_BASE_PROMPT, output_type=chat_output)
srs_structured_agent = Agent("groq:gemma2-9b-it", output_type=SRSInput)

# Instruction with reasoning mode


async def srs_conversation():
    print("\n💬 Starting SRS Q&A (AI with reasoning)...\n")
    history = SRS_BASE_PROMPT.strip() + "\n\n"
    while True:
        response = await srs_chat_agent.run(history)
        full_reply = response.output.question.strip()
        if "all done" in full_reply.lower():
            break
        print(f"🤖 AI: {full_reply}")
        user_input = input("🧑 You: ").strip()
        if user_input.lower() == "exit":
            print("👋 Exiting...")
            return
        history += f"Assistant: {full_reply}\nUser: {user_input}\n"
    print("\n🧠 Generating structured SRS...\n")
    final_result = await srs_structured_agent.run(history)
    srs = final_result.output
    print("✅ Final SRS (Structured):")
    print(json.dumps(srs.model_dump(), indent=2))

def main():
    print("🧠 Dynamic AI Proposal Generator (Gemini-powered)")
    print(" 1: Start SRS Q&A (AI-guided)")
    print(" 0: Exit")

    while True:
        choice = input("Select option (0, 1 or 2): ").strip()
        if choice == "1":
            asyncio.run(srs_conversation())
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid option. Please enter 0, 1 or 2.")

if __name__ == "__main__":
    main()
