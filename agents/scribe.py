# Scribe Agent - Part of the MeetIQ Multi-Agent Pipeline
# This agent handles parsing, cleaning, and structuring of raw conversational text.

import os
from google.adk import Agent
from google.genai import types

def get_scribe_agent() -> Agent:
    """
    Architectural Design:
    The Scribe Agent serves as Agent 1 in our pipeline. It takes the raw, unstructured, 
    and noisy meeting transcript and outputs a clean, speaker-tagged, and linguistically 
    standardized transcript. This prepares the text for downstream extraction and auditing.
    
    Rubric Compliance:
    - Modular file structure.
    - Clear division of agent responsibilities.
    - Specific system instructions addressing Indian corporate jargon (Hinglish).
    """
    
    # Detailed instructions instructing Gemini to restructure Hinglish jargon and identify speakers
    instruction = (
        "You are the Scribe Agent, a highly skilled corporate communications analyst.\n"
        "Your task is to take a raw, messy, and unstructured meeting transcript and clean it up.\n\n"
        "Follow these rules strictly:\n"
        "1. SPEAKER IDENTIFICATION: Identify the speaker of each utterance. Format the output cleanly "
        "as: '[Speaker Name] ([Role]): [Cleaned Utterance]' or '[Speaker Name]: [Cleaned Utterance]'.\n"
        "2. INDIAN CORPORATE JARGON CLEANUP: Identify and translate commonly used Indian corporate jargon "
        "or Hinglish/Indianisms into standard global corporate English. Examples:\n"
        "   - Replace 'do the needful' with 'take the necessary action' or 'handle this'.\n"
        "   - Replace 'prepone' with 'bring forward' or 'move to an earlier time'.\n"
        "   - Replace 'revert back' with 'reply' or 'get back to'.\n"
        "   - Replace 'discuss about' with 'discuss'.\n"
        "   - Replace 'out of station' with 'out of town' or 'away'.\n"
        "   - Replace 'bandwidth is choked' with 'capacity is fully booked' or 'too busy'.\n"
        "   - Replace 'prepone' or 'preponing' with 'rescheduling earlier' or 'bringing forward'.\n"
        "3. NOISE REDUCTION: Remove non-value-adding verbal fillers ('um', 'ah', 'yaar', 'ya', 'actually'), "
        "conversational stuttering, and off-topic greetings, while preserving the exact technical constraints, "
        "blockers, task allocations, and dates mentioned.\n"
        "4. FLOW AND STRUCTURE: Present the cleaned transcript in chronological order of dialogue. "
        "Ensure it is highly readable, structured, and professional."
    )

    # We use gemini-2.5-flash for fast, cost-effective transcript structuring.
    agent = Agent(
        name="ScribeAgent",
        model="gemini-2.5-flash",
        instruction=instruction
    )
    return agent
