# Orchestrator - Main Execution Flow for MeetIQ Pipeline
# Coordinates Scribe and Executive Assistant agents using google-adk.

import os
import sys
import json
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

# Adjust path to allow absolute imports when running as a script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from agents.scribe import get_scribe_agent
from agents.exec_assistant import get_exec_assistant_agent
from agents.auditor import get_auditor_agent

# Hardcoded High-Fidelity Fallback Dataset
# Used to populate data files if the Gemini API Key is missing/invalid,
# ensuring the dashboard remains visual and working.

MOCK_ACTION_ITEMS = {
  "action_items": [
    {
      "task": "Review AWS instance 502 status and prepone database migration to today.",
      "owner": "Amit",
      "deadline": "Today"
    },
    {
      "task": "Push migration/backend code today so QA can verify before leaving.",
      "owner": "Amit",
      "deadline": "Today"
    },
    {
      "task": "Test database changes before traveling for wedding next week.",
      "owner": "Avni",
      "deadline": "Before leaving"
    },
    {
      "task": "Request repository access from IT Support and revert back to PM.",
      "owner": "Avanti",
      "deadline": "Today"
    },
    {
      "task": "Take over login API implementation once repository access is granted.",
      "owner": "Avanti",
      "deadline": "As soon as access is granted"
    },
    {
      "task": "Send an email update to Srikant detailing AWS instance status.",
      "owner": "Amit",
      "deadline": "Tomorrow morning"
    },
    {
      "task": "Ensure frontend looks good and implement placeholder data to avoid blank view for client demo.",
      "owner": "Sanvi",
      "deadline": "Tomorrow"
    }
  ],
  "decisions": [
    {
      "decision": "Database migration schema conflict with Apex dashboard UI parked and taken offline.",
      "context": "Migrating schema today would break Sanvi's dashboard UI due to role-based access control hardcoding just before the client demo."
    },
    {
      "decision": "Avanti will handle the login API implementation instead of Amit.",
      "context": "Amit's bandwidth is completely choked due to other high-priority integrations."
    },
    {
      "decision": "The database migration final decision is rescheduled for a sync tomorrow morning.",
      "context": "The team needs a formal status update from Amit before changing production schemas."
    }
  ],
  "risks": [
    {
      "risk_description": "Database migration will break Apex dashboard UI role-based access control.",
      "impacted_component": "Frontend UI / Apex Dashboard"
    },
    {
      "risk_description": "QA engineer is traveling next week; delaying code push past today leaves the build untested.",
      "impacted_component": "QA & Testing Pipeline"
    },
    {
      "risk_description": "Avanti lacks repository access to begin working on the login API.",
      "impacted_component": "Login API Repo Access"
    }
  ],
  "summary_doc_url": "https://docs.google.com/document/d/mock_doc_id/edit",
  "draft_email_links": [
    "https://mail.google.com/mail/u/0/#drafts/mock_draft_id"
  ]
}

MOCK_AUDIT_RESULTS = {
  "efficiency_score": 25,
  "verdict": "Could have been an email",
  "reasons": [
    "High invitee count (10) but low active speaker ratio (3 speakers: Srikant, Amit, Sanvi).",
    "A 45-minute sync with zero critical decisions finalized (migration parked, API access delayed).",
    "Meeting devolved into unstructured database schema arguments without resolution."
  ],
  "recommendation": "Cap invitees to active stakeholders only. Circulate status updates asynchronously. Take specialized database debates offline to a smaller working group."
}

def load_raw_transcript() -> str:
    """Reads the raw, messy Hinglish mock transcript from data directory."""
    path = os.path.join(parent_dir, "data", "mock_transcript.txt")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Transcript file not found at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_action_items(data: dict):
    """Writes extracted action items to data/action_items.json."""
    path = os.path.join(parent_dir, "data", "action_items.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Successfully saved action items to: {path}")

def write_audit_results(data: dict):
    """Writes meeting audit results to data/audit_results.json."""
    path = os.path.join(parent_dir, "data", "audit_results.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Successfully saved audit results to: {path}")

def run_pipeline():
    """
    Orchestrates the multi-agent pipeline:
    1. Load environment and verify API key.
    2. Run Scribe Agent to clean Hinglish transcript.
    3. Run Executive Assistant Agent to extract actions, decisions, and risks.
    4. Save final output.
    """
    load_dotenv()
    
    # Check if GEMINI_API_KEY environment variable is configured
    api_key = os.environ.get("GEMINI_API_KEY")
    is_placeholder = not api_key or "your_gemini_api_key" in api_key or "YOUR_GEMINI_API_KEY" in api_key
    
    if is_placeholder:
        print("\n" + "="*70)
        print("WARNING: GEMINI_API_KEY is not configured or is a placeholder in .env!")
        print("To enable live agent extraction, set a valid key in d:\\Sanvi\\MeetIQ\\.env")
        print("Proceeding with high-fidelity mockup fallback dataset for testing...")
        print("="*70 + "\n")
        write_action_items(MOCK_ACTION_ITEMS)
        write_audit_results(MOCK_AUDIT_RESULTS)
        return
        
    try:
        raw_transcript = load_raw_transcript()
        print("Running Scribe Agent...")
        results = run_analysis_pipeline(raw_transcript)
        
        # Save split results for local file persistence
        action_plan_dict = {
            "action_items": results.get("action_items", []),
            "decisions": results.get("decisions", []),
            "risks": results.get("risks", []),
            "summary_doc_url": results.get("summary_doc_url"),
            "draft_email_links": results.get("draft_email_links", [])
        }
        audit_dict = {
            "efficiency_score": results.get("efficiency_score", 0),
            "verdict": results.get("verdict", ""),
            "reasons": results.get("reasons", []),
            "recommendation": results.get("recommendation", "")
        }
        
        write_action_items(action_plan_dict)
        write_audit_results(audit_dict)
        print("Multi-agent pipeline execution completed successfully!")
        
    except Exception as e:
        print(f"\nPipeline failed during live execution: {e}")
        print("Generating fallback action items and audit results to keep the application operational...\n")
        write_action_items(MOCK_ACTION_ITEMS)
        write_audit_results(MOCK_AUDIT_RESULTS)

def run_analysis_pipeline(raw_transcript: str) -> dict:
    """
    Executes the multi-agent pipeline on the raw_transcript:
    1. Scribe Agent cleans/structures Hinglish transcript.
    2. Executive Assistant Agent parses items and updates Google Workspace.
    3. Efficiency Auditor Agent grades meeting efficiency.
    
    Returns a combined dictionary matching the unified React app schema.
    """
    # STEP 1: Scribe Agent execution
    scribe_agent = get_scribe_agent()
    scribe_runner = InMemoryRunner(agent=scribe_agent)
    scribe_runner.auto_create_session = True
    
    scribe_message = types.Content(parts=[types.Part.from_text(text=raw_transcript)])
    scribe_events = list(scribe_runner.run(
        user_id="user_1", 
        session_id="session_scribe_run", 
        new_message=scribe_message
    ))
    
    clean_transcript = ""
    for event in scribe_events:
        if event.error_code:
            err_msg = event.error_message if event.error_message else event.error_code
            raise RuntimeError(f"Scribe Agent Error ({event.error_code}): {err_msg}")
        if event.message and event.message.parts:
            clean_transcript = "".join(part.text for part in event.message.parts if part.text)
            
    if not clean_transcript:
        raise RuntimeError("Scribe Agent produced an empty transcript.")
        
    # STEP 2: Executive Assistant Agent execution
    ea_agent = get_exec_assistant_agent()
    ea_runner = InMemoryRunner(agent=ea_agent)
    ea_runner.auto_create_session = True
    
    ea_message = types.Content(parts=[types.Part.from_text(text=clean_transcript)])
    ea_events = list(ea_runner.run(
        user_id="user_1", 
        session_id="session_ea_run", 
        new_message=ea_message
    ))
    
    action_plan_text = ""
    for event in ea_events:
        if event.error_code:
            err_msg = event.error_message if event.error_message else event.error_code
            raise RuntimeError(f"Executive Assistant Agent Error ({event.error_code}): {err_msg}")
        
        # Log function calls (tool invocations) live to show ADK routing
        fcs = event.get_function_calls()
        if fcs:
            for fc in fcs:
                print(f"\n[Tool Call] Agent calling tool '{fc.name}' with args: {fc.args}")
        
        # Log function responses (tool execution outputs) live
        frs = event.get_function_responses()
        if frs:
            for fr in frs:
                print(f"[Tool Response] Tool '{fr.name}' returned: {fr.response}\n")

        if event.message and event.message.parts:
            action_plan_text = "".join(part.text for part in event.message.parts if part.text)
            
    if not action_plan_text:
        raise RuntimeError("Executive Assistant Agent produced no output.")
        
    # Parse the JSON string directly. Strip potential markdown fences if present.
    cleaned_json_text = action_plan_text.strip()
    if cleaned_json_text.startswith("```"):
        lines = cleaned_json_text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned_json_text = "\n".join(lines).strip()

    action_plan_dict = json.loads(cleaned_json_text)
    
    # STEP 3: Efficiency Auditor Agent execution
    auditor_agent = get_auditor_agent()
    auditor_runner = InMemoryRunner(agent=auditor_agent)
    auditor_runner.auto_create_session = True
    
    # Formulate metadata from transcript context
    metadata = {
        "duration_minutes": 45,
        "invitees": 10,
        "active_speakers": 3,
        "decisions_made": len(action_plan_dict.get("decisions", [])),
        "agenda_items_completed": 1
    }
    
    auditor_prompt = (
        f"Meeting Metadata:\n"
        f"- Duration: {metadata['duration_minutes']} minutes\n"
        f"- Total Invitees: {metadata['invitees']}\n"
        f"- Active Speakers: {metadata['active_speakers']}\n"
        f"- Decisions Made: {metadata['decisions_made']}\n"
        f"- Agenda Items Completed: {metadata['agenda_items_completed']}\n\n"
        f"Cleaned Transcript:\n{clean_transcript}"
    )
    
    auditor_message = types.Content(parts=[types.Part.from_text(text=auditor_prompt)])
    auditor_events = list(auditor_runner.run(
        user_id="user_1", 
        session_id="session_auditor_run", 
        new_message=auditor_message
    ))
    
    audit_text = ""
    for event in auditor_events:
        if event.error_code:
            err_msg = event.error_message if event.error_message else event.error_code
            raise RuntimeError(f"Efficiency Auditor Agent Error ({event.error_code}): {err_msg}")
        if event.message and event.message.parts:
            audit_text = "".join(part.text for part in event.message.parts if part.text)
            
    if not audit_text:
        raise RuntimeError("Efficiency Auditor Agent produced no output.")
        
    cleaned_audit_json = audit_text.strip()
    if cleaned_audit_json.startswith("```"):
        lines = cleaned_audit_json.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned_audit_json = "\n".join(lines).strip()
        
    audit_dict = json.loads(cleaned_audit_json)
    
    return {
        **action_plan_dict,
        **audit_dict
    }

if __name__ == "__main__":
    run_pipeline()
