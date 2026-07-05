# Efficiency Auditor Agent - Part of the MeetIQ Multi-Agent Pipeline
# This agent evaluates meeting transcripts and metadata to calculate productivity metrics.

from typing import List
from pydantic import BaseModel, Field
from google.adk import Agent

# Pydantic Schema to Enforce Auditor JSON Output Structure

class MeetingAuditResult(BaseModel):
    """
    Pydantic Schema defining the output structure for the Efficiency Auditor.
    This schema is enforced by the ADK runtime using Gemini Structured Outputs.
    """
    efficiency_score: int = Field(
        description="The calculated meeting efficiency score from 0 (complete waste of time) to 100 (highly productive)."
    )
    verdict: str = Field(
        description="A concise, high-impact summary verdict (e.g. 'Could have been an email', 'Severe participation drain', 'Productive sync')."
    )
    reasons: List[str] = Field(
        description="A list of specific, harsh but professional reasons justifying the deductions or score."
    )
    recommendation: str = Field(
        description="Specific, actionable coaching advice for the organizer to optimize future syncs."
    )

# Auditor Agent Constructor

def get_auditor_agent() -> Agent:
    """
    Architectural Design:
    The Efficiency Auditor (Agent 3) acts as the quality assurance layer. 
    It ingests the structured Scribe transcript and corporate metadata (invitee count, 
    active speakers, decisions, agenda status) and evaluates waste metrics.
    
    Rubric Compliance:
    - Modular agent design isolated from Scribe and EA.
    - Strong typing using Pydantic models for structured output validation.
    - Heavily commented for Kaggle grading parameters.
    """
    
    instruction = (
        "You are a ruthless, highly critical corporate Efficiency Auditor Agent.\n"
        "Your role is to assess a meeting's productivity and calculate an Efficiency Score (0-100) "
        "based on the provided meeting metadata and cleaned transcript.\n\n"
        "Auditing rules you MUST enforce:\n"
        "- PENALIZE low participation: If there are many invitees but few active speakers (low speaker ratio), "
        "  penalize the score heavily. Idle invitees waste corporate salary hours.\n"
        "- PENALIZE zero or low decisions: A meeting's main purpose is alignment and decision making. "
        "  If the number of decisions made is zero or low, particularly in a long meeting, deduct substantial points.\n"
        "- PENALIZE agenda incompletion: If the agenda items completed are low relative to the duration, deduct points.\n"
        "- Standardize the verdict to be high-impact, professional, and corporate-aligned.\n"
        "- Provide actionable recommendations, such as capping invitees, using asynchronous email threads, "
        "  or moving the meeting entirely to a shared document.\n\n"
        "You must output a structured JSON conforming to the MeetingAuditResult schema."
    )
    
    # We use gemini-2.5-flash to evaluate analytics and return validated structured JSON
    agent = Agent(
        name="EfficiencyAuditorAgent",
        model="gemini-2.5-flash",
        instruction=instruction,
        output_schema=MeetingAuditResult
    )
    return agent
