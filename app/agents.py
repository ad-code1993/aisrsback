import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from pydantic_ai import Agent
from typing import Optional
from .models import SRSInput
import json
from pydantic_ai.models.groq import GroqModel
load_dotenv()

# Agent configuration

AGENT_MODEL = GroqModel(
    "llama-3.3-70b-versatile"
)

# Enhanced SRS Base Prompt with stricter instructions
SRS_BASE_PROMPT = """
You are a systematic requirements gathering assistant. Your task is to collect information for a Software Requirements Specification (SRS) document by asking one question at a time.

RULES:
1. Ask only ONE question per response
2. Always provide both 'reason' and 'question'
3. Use the exact JSON format specified below
4. When all information is collected, respond with "All done" in the question field

FIELDS TO COLLECT (ask about these in logical order):
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

STRICT RESPONSE FORMAT (JSON ONLY):
{
  "reason": "Brief explanation of why this information is needed",
  "question": "The specific question to ask about this field"
}

EXAMPLE:
{
  "reason": "The project name identifies the system being developed",
  "question": "What is the name of this project?"
}

DO NOT include any additional text, markdown, or formatting outside the JSON object.
"""

# Chat Output Model
class ChatOutput(BaseModel):
    reason: str = Field(..., description="Reasoning behind the question")
    question: str = Field(..., description="The question asked by the AI")

def validate_response(response) -> ChatOutput:
    """Validate and parse the agent response, handling multiple formats."""
    # If response is already a ChatOutput object, return it
    if isinstance(response, ChatOutput):
        return response
    
    # If response is an object with output attribute
    if hasattr(response, 'output'):
        if isinstance(response.output, ChatOutput):
            return response.output
        response_text = str(response.output)
    else:
        response_text = str(response)

    # Clean the response text
    response_text = response_text.strip()
    
    # Remove JSON code fences if present
    if response_text.startswith("```json"):
        response_text = response_text[7:-3].strip()
    elif response_text.startswith("```"):
        response_text = response_text[3:-3].strip()

    try:
        # Try to parse as JSON
        if response_text.startswith('{') and response_text.endswith('}'):
            data = json.loads(response_text)
            return ChatOutput(**data)
        
        # Fallback for malformed but parsable responses
        if '"reason"' in response_text and '"question"' in response_text:
            try:
                data = json.loads(response_text[response_text.index('{'):response_text.rindex('}')+1])
                return ChatOutput(**data)
            except:
                pass

        # Try to extract from text format
        reason = None
        question = None
        
        if "reason:" in response_text.lower():
            reason_part = response_text[response_text.lower().index("reason:") + 7:].strip()
            reason = reason_part.split("\n")[0].strip(" '\"")
        
        if "question:" in response_text.lower():
            question_part = response_text[response_text.lower().index("question:") + 9:].strip()
            question = question_part.split("\n")[0].strip(" '\"")

        if reason and question:
            return ChatOutput(reason=reason, question=question)
        
        # Final fallback
        return ChatOutput(
            reason="We need to collect project information",
            question="What is the name of this project?"
        )
        
    except Exception as e:
        # Ultimate fallback if all parsing fails
        return ChatOutput(
            reason="We need to establish basic project information",
            question="Could you please tell me the name of this project?"
        )

# Create agents with enhanced configuration
srs_chat_agent = Agent(
    AGENT_MODEL,
    system_prompt=SRS_BASE_PROMPT,
    output_type=ChatOutput,
)

srs_structured_agent = Agent(
    AGENT_MODEL,
    output_type=SRSInput,
)

srs_agent = Agent(
    AGENT_MODEL
)

# Format prompt for SRS document generation
srs_agent = Agent(
    AGENT_MODEL,
    retries=5,
    )

def format_srs_prompt(data: SRSInput) -> str:
    """Generate a comprehensive SRS document utilizing all fields"""
    return f"""
You are a senior technical writer creating a formal Software Requirements Specification document.
Produce a complete, professional SRS that would span 4-12 pages when formatted, using all provided information.

STRUCTURE THE DOCUMENT AS FOLLOWS:

# 1. PROJECT IDENTIFICATION

## 1.1 Basic Metadata
- **Project Name**: {data.project_name}
  - Alternative names/codenames
  - Project classification (internal/client-facing/open-source)
  
- **SRS Version**: {data.srs_version}
  - Version control methodology
  - Change management process

- **Creation Date**: {data.creation_date}
  - Revision history
  - Planned review cycles

## 1.2 Authorship & Stakeholders
- **Authors**: {data.authors}
  - For each author:
    * Role and responsibilities
    * Contact information
    * Organizational unit

- **Stakeholders**: {data.stakeholders}
  - Stakeholder matrix:
    * Interest level
    * Influence level
    * Communication needs
  - Decision-making hierarchy

- **Expected Release**: {data.expected_release_date}
  - Key milestones
  - Critical path analysis
  - Risk mitigation timeline

# 2. INTRODUCTION

## 2.1 Purpose & Scope
- **Document Purpose**: {data.srs_purpose}
  - Intended usage scenarios
  - Compliance requirements
  - Reference documents

- **System Purpose**: {data.main_purpose}
  - Business objectives
  - Success metrics (KPIs)
  - Value proposition

- **Scope**: {data.scope}
  - System boundaries
  - Interfaces with other systems
  - Scope visualization (diagram description)

## 2.2 Background
- **Overview**: {data.overview_summary}
  - Business context
  - Technical landscape
  - Strategic alignment

- **Problem Statement**: {data.problem}
  - Root cause analysis
  - Impact quantification
  - Current workarounds

# 3. DEFINITIONS & REFERENCE

## 3.1 Terminology
- **Acronyms**: {data.acronyms}
  - Full definitions
  - Usage context
  - Related terms

## 3.2 References
- Standards compliance
- Regulatory framework
- Technical references

# 4. USER CHARACTERISTICS

- **Intended Users**: {data.intended_users}
  - User personas (3-5 detailed profiles)
  - For each:
    * Demographics
    * Technical proficiency
    * Usage patterns
    * Special needs

- **Affected Parties**: {data.affected_parties}
  - Indirect users
  - Business units impacted
  - External systems affected

# 5. REQUIREMENTS

## 5.1 Functional Requirements
- **Major Features**: {data.major_features}
  - Feature breakdown:
    * Description
    * User stories
    * Acceptance criteria
    * Dependencies

- **MVP Definition**: {data.mvp}
  - Core feature set
  - Minimum viable quality
  - Phase 1 deliverables

## 5.2 Data Requirements
- **Database Design**: {data.db_design}
  - Entity relationships
  - Data flow diagrams
  - Storage requirements

- **Datasheets**: {data.datasheets}
  - Technical specifications
  - Performance characteristics
  - Interface protocols

## 5.3 Interface Requirements
- **UI/UX Design**: {data.uiux}
  - Wireframe descriptions
  - Navigation flows
  - Accessibility standards

# 6. CONSTRAINTS

## 6.1 Technical Constraints
- **Resources**: {data.resources}
  - Hardware limitations
  - Software dependencies
  - Team capacity

- **Constraints**: {data.constraints}
  - Architectural decisions
  - Technology stack
  - Integration limitations

## 6.2 Business Constraints
- Budget limitations
- Timeline restrictions
- Compliance requirements

# 7. SOLUTION APPROACH

## 7.1 Ideal Solution
- **Vision**: {data.ideal_solution}
  - Future state architecture
  - Scalability considerations
  - Innovation opportunities

## 7.2 Deliverables
- **Deliverables**: {data.deliverables}
  - Artifact list with descriptions
  - Quality metrics
  - Acceptance criteria

- **Delivery Stages**: {data.delivery_stages}
  - Phase definitions
  - Milestone schedule
  - Success indicators

# 8. SUPPLEMENTAL INFORMATION

## 8.1 Assumptions
- **Assumptions**: {data.assumptions}
  - For each assumption:
    * Rationale
    * Validation method
    * Impact if invalid

## 8.2 Future Considerations
- **Rabbit Holes**: {data.rabbit_holes}
  - Potential extensions
  - Research areas
  - Innovation opportunities

## 8.3 Limitations
- **Out of Scope**: {data.out_of_scope}
  - Specific exclusions
  - Justification
  - Future consideration

- **Restrictions**: {data.restrictions}
  - Technical prohibitions
  - Business limitations
  - Compliance boundaries

# 9. IMPACT ANALYSIS

- **Impacts**: {data.impacts}
  - Business processes affected
  - Technical debt implications
  - Organizational change required

DOCUMENTATION STANDARDS:
1. Use IEEE SRS format conventions
2. Number all requirements (REQ-001, etc.)
3. Include traceability matrix
4. Use consistent heading hierarchy
5. Maintain professional technical tone
6. Aim for 3000-5000 words total
7. Include [TBD] markers for missing info
8. All requirements must be testable
9. Use tables for complex relationships
10. Provide examples where helpful

OUTPUT FORMAT:
Key points for the renderer:
1. Tables will get automatic styling with borders and hover effects
2. Code blocks will get syntax highlighting
3. Math expressions will be rendered with KaTeX
4. Headings will have consistent sizing and spacing
5. Lists will have proper indentation and spacing

The renderer will automatically:
- Process frontmatter if present
- Format tables correctly
- Apply consistent styling
- Handle math expressions
- Maintain proper spacing and hierarchy
# Ensure the SRS is comprehensive, structured, and professional.
- Complete Markdown document
- Proper section numbering
- Consistent bullet point formatting
- Clear separation of concerns
- Unambiguous requirement statements
"""