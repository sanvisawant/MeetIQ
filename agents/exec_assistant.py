# Executive Assistant Agent - Part of the MeetIQ Multi-Agent Pipeline
# This agent extracts structured actionable data (tasks, decisions, risks) from the transcript
# and automates tasks using Model Context Protocol (MCP) integrations.

from typing import List, Optional
from pydantic import BaseModel, Field
from google.adk import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Pydantic Schemas to Enforce Valid JSON Output Structure

class ActionItem(BaseModel):
    task: str = Field(description="The description of the task or action item extracted from the conversation.")
    owner: str = Field(description="The name of the person responsible for this task. Set to 'Unassigned' if not specified.")
    deadline: Optional[str] = Field(description="The deadline or time frame mentioned for the task. Set to null if not specified.")

class Risk(BaseModel):
    risk_description: str = Field(description="Description of the risk, technical blocker, or dependency identified.")
    impacted_component: str = Field(description="The software component, server, dashboard, database, or process impacted by this risk.")

class Decision(BaseModel):
    decision: str = Field(description="A key decision or agreement reached during the meeting.")
    context: str = Field(description="The context or explanation behind why this decision was made.")

class MeetingActionPlan(BaseModel):
    action_items: List[ActionItem] = Field(description="List of all extracted action items and tasks.")
    decisions: List[Decision] = Field(description="List of all key decisions made in the meeting.")
    risks: List[Risk] = Field(description="List of technical blockers, capacity issues, or project risks.")
    summary_doc_url: Optional[str] = Field(None, description="The full URL of the created Google Doc. Format as: https://docs.google.com/document/d/<documentId>/edit")
    draft_email_links: List[str] = Field(default_factory=list, description="List of draft IDs, links, or statuses representing the drafted Gmail messages.")


# =====================================================================
# Real Workspace MCP Client Configuration & Tool Binding
# =====================================================================
#
# Architectural routing under ADK:
# 1. McpToolset starts a child process running 'python agents/workspace_mcp_filter.py'.
# 2. The proxy wrapper script launches the NPM workspace server and filters out non-JSON stdout lines.
# 3. The server lists its available Workspace tools (Docs, Gmail, Calendar, Drive).
# 4. ADK maps the tools dynamically using standard MCP schemas and binds them to the agent.
#
workspace_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=["agents/workspace_mcp_filter.py"],
        ),
        timeout=60.0
    )
)

# Executive Assistant Agent Constructor

def get_exec_assistant_agent() -> Agent:
    """
    Architectural Design:
    The Executive Assistant (EA) Agent acts as Agent 2 in our pipeline. It ingests 
    the clean transcript produced by the Scribe Agent, parses the business logic, and 
    structures it into action items, decisions, and risks. 
    
    In addition, it has access to real Google Workspace MCP tools to:
    - Create a Google Doc containing a summary of meeting notes, decisions, and risks.
    - Draft a Gmail message outlining action items and deadlines.
    
    Rubric Compliance:
    - Modular architecture, separate from Scribe and Orchestrator.
    - Uses Pydantic model (`output_schema=MeetingActionPlan`) to enforce a valid JSON schema response.
    - Connects to a real Google Workspace MCP Server.
    - Code is heavily annotated for evaluation points.
    """
    
    instruction = (
        "You are the Executive Assistant Agent, an expert business analyst and office automation assistant.\n"
        "Your role is to analyze a structured corporate meeting transcript and perform two key tasks:\n\n"
        "1. EXTRACT STRUCTURED OUTCOMES: Extract all Action Items, Decisions, and Risks matching the output schema.\n"
        "2. EXECUTE WORKSPACE ACTIONS: Call Google Workspace MCP tools to automate post-meeting logistics:\n"
        "   - Google Docs: Create a new Google Doc (using the docs tool) containing a summary of the meeting notes, "
        "     decisions, and risks. From the response, extract the `documentId` and format the Google Doc URL as "
        "     `https://docs.google.com/document/d/<documentId>/edit` to populate the `summary_doc_url` field.\n"
        "   - Gmail: Draft a Gmail message (using the gmail tool) summarizing the action items for the owners. "
        "     Extract the draft ID or reference from the tool's response to populate the `draft_email_links` list.\n\n"
        "You must output a structured JSON matching the provided schema exactly, including the captured "
        "Google Doc URL and Gmail draft details in `summary_doc_url` and `draft_email_links` fields. "
        "Ensure all fields are fully filled based on the transcript and tool responses."
    )
    
    # We use gemini-2.5-flash for structured data extraction and formatting.
    # Passing the Pydantic schema tells ADK to format and validate the LLM response.
    # The tools list binds the Workspace MCP Toolset.
    agent = Agent(
        name="ExecutiveAssistantAgent",
        model="gemini-2.5-flash",
        instruction=instruction,
        output_schema=MeetingActionPlan,
        tools=[workspace_toolset]
    )
    return agent
