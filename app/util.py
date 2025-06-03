from typing import Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Step 1: Define proposal input model


# Step 3: Create the Gemini AI agent


class SRSInput(BaseModel):
    project_name: str = Field(..., description="Project name")
    srs_version: str = Field(..., description="Version of the SRS document")
    authors: str = Field(..., description="Authors or contributors")
    creation_date: str = Field(..., description="Date of creation")
    stakeholders: str = Field(..., description="Stakeholders involved")
    expected_release_date: str = Field(..., description="Expected delivery or release date")
    overview_summary: str = Field(..., description="Brief summary of the system")
    main_purpose: str = Field(..., description="Main purpose of the project")
    intended_users: str = Field(..., description="Intended users or beneficiaries")
    srs_purpose: str = Field(..., description="Purpose of this SRS document")
    scope: str = Field(..., description="Scope of the software system")
    assumptions: str = Field(..., description="Assumptions, dependencies, or constraints")
    acronyms: str = Field(..., description="Acronyms, abbreviations, or references to explain")
    problem: str = Field(..., description="Problem or challenge addressed")
    affected_parties: str = Field(..., description="Who is affected and in what context")
    impacts: str = Field(..., description="Impacts or inefficiencies caused by current state")
    resources: str = Field(..., description="Resources and time allocated")
    constraints: str = Field(..., description="Budgetary or technical constraints")
    mvp: str = Field(..., description="Minimum viable solution")
    ideal_solution: str = Field(..., description="Ideal solution if no constraints")
    deliverables: str = Field(..., description="Expected deliverables of the system")
    delivery_stages: str = Field(..., description="Important delivery stages or milestones")
    major_features: str = Field(..., description="Major features or capabilities planned")
    datasheets: str = Field(..., description="Technical specifications or datasheets")
    db_design: str = Field(..., description="Main entities/tables and relationships")
    uiux: str = Field(..., description="UI/UX design details")
    rabbit_holes: str = Field(..., description="Feature ideas or areas for future exploration")
    out_of_scope: str = Field(..., description="Explicitly out of scope items")
    restrictions: str = Field(..., description="Technologies/methods/tools not to be used or legal/ethical restrictions")

# Step 6: Create the Gemini AI agent for SRS
srs_agent = Agent("groq:llama-3.3-70b-versatile")

# Step 7: Format prompt for SRS document generation

def format_srs_prompt(data: SRSInput) -> str:
    return f"""
You are a professional technical writer. Write a detailed Software Requirements Specification (SRS) document using the following structure:

# 1. Project Metadata
- Project Name: {data.project_name}
- SRS Version: {data.srs_version}
- Authors: {data.authors}
- Date of Creation: {data.creation_date}
- Stakeholders: {data.stakeholders}
- Expected Delivery/Release Date: {data.expected_release_date}

# 2. Overview
- Summary: {data.overview_summary}
- Main Purpose: {data.main_purpose}
- Intended Users/Beneficiaries: {data.intended_users}

# 3. Introduction
- Purpose of this SRS: {data.srs_purpose}
- Scope: {data.scope}
- Assumptions/Dependencies/Constraints: {data.assumptions}
- Acronyms/Abbreviations/References: {data.acronyms}

# 4. Identified Problem
- Problem/Challenge: {data.problem}
- Affected Parties/Context: {data.affected_parties}
- Impacts/Inefficiencies: {data.impacts}

# 5. Appetite
- Resources/Time Allocated: {data.resources}
- Budgetary/Technical Constraints: {data.constraints}
- Minimum Viable Solution: {data.mvp}
- Ideal Solution (if no constraints): {data.ideal_solution}

# 6. Solution Concept
## 6.1 Description of Deliverables
- Deliverables: {data.deliverables}
- Delivery Stages/Milestones: {data.delivery_stages}
## 6.2 Major Features
{data.major_features}
## 6.3 Design Documents
- Datasheets/Technical Specs: {data.datasheets}
- Database Design: {data.db_design}
- UI/UX Design: {data.uiux}

# 7. Rabbit Holes
- Feature Ideas/Areas for Future Exploration: {data.rabbit_holes}

# 8. No-gos
- Out of Scope: {data.out_of_scope}
- Restrictions (Technologies/Methods/Legal/Ethical): {data.restrictions}

Write in a professional tone, using clear section headings and bullet points where appropriate.
Ensure the SRS flows logically from project context to solution details.
"""

# Step 8: Generate SRS document
async def generate_srs():
    # You would collect SRSInput data from user or another source
    # For demonstration, you can create a sample SRSInput instance or pass as argument
    # srs_input = SRSInput(...)
    # prompt = format_srs_prompt(srs_input)
    # result = await srs_agent.run(prompt)
    # print("\n📄 Generated SRS Document:\n")
    # print(result.output)
    pass
