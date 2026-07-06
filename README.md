<div align="center">

# 🚀 MeetIQ

### AI-Powered Meeting Intelligence & Workspace Automation

Transform conversations into execution with **Multi-Agent AI**, **Google ADK**, and the **Model Context Protocol (MCP)**.

<p>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge)
![Google ADK](https://img.shields.io/badge/Google-ADK-EA4335?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-Integrated-34A853?style=for-the-badge)

</p>

*Built for the Kaggle AI Agents: Intensive Vibe Coding Capstone.*

</div>

---

# 📌 The Problem

Modern organizations spend countless hours in meetings, yet much of that time is lost due to:

- Unclear action items
- Forgotten decisions
- Manual meeting notes
- Delayed follow-up emails
- No accountability
- Inefficient meetings with little measurable outcome

While AI meeting summarizers generate notes, **they rarely automate what happens next.**

---

# 💡 Our Solution

MeetIQ is an **AI Meeting Intelligence Platform** powered by a **multi-agent architecture**.

Instead of simply summarizing meetings, MeetIQ understands discussions, extracts actionable insights, measures meeting effectiveness, and automates post-meeting workflows using Google Workspace.

It transforms meetings into an execution pipeline.

<h2>🏗️ Workflow</h2>

<table>
<tr>
<td align="center"><b>📥<br>Meeting Transcript</b></td>
<td align="center">➡️</td>
<td align="center"><b>📝<br>Scribe Agent</b></td>
<td align="center">➡️</td>
<td align="center"><b>📋<br>Executive Assistant</b></td>
<td align="center">➡️</td>
<td align="center"><b>☁️<br>Google Workspace MCP</b></td>
<td align="center">➡️</td>
<td align="center"><b>📄<br>Google Docs<br>Gmail</b></td>
<td align="center">➡️</td>
<td align="center"><b>📊<br>Efficiency Auditor</b></td>
<td align="center">➡️</td>
<td align="center"><b>📈<br>Meeting Dashboard</b></td>
</tr>
</table>

---

# ✨ Key Features

- 🧠 Multi-Agent AI Architecture
- 📝 Intelligent Transcript Structuring
- ✅ Action Item Extraction
- 📌 Decision Detection
- ⚠️ Risk Identification
- 👤 Owner Assignment
- 📧 Automated Follow-up Email Drafting
- 📄 Google Docs Meeting Summary
- 📊 Meeting Efficiency Score
- 🔗 Google Workspace Integration (MCP)
- 🔒 Secure OAuth Authentication
- ⚡ Graceful Mock Fallbacks

---

# 🎯 Why AI Agents?

Traditional LLM applications stop after generating text.

MeetIQ goes one step further.

Each agent has a dedicated responsibility, collaborates with other agents, and interacts with external productivity tools through MCP.

This enables the system to:

- Reason about meeting content
- Divide responsibilities
- Execute actions
- Automate workflows
- Produce measurable business outcomes

MeetIQ is not a chatbot.

It is an autonomous meeting operations assistant.

---

# 🏗️ Architecture

<img width="1672" height="941" alt="ChatGPT Image Jul 7, 2026, 02_50_02 AM" src="https://github.com/user-attachments/assets/4ccccf78-e2c6-4736-b40e-4b4ffb77f92f" />



MeetIQ follows a modular three-agent architecture built using Google's Agent Development Kit (ADK).

---

## 📝 Agent 1 — Scribe Agent

**Responsibility**

Convert raw meeting transcripts into structured, machine-readable conversations.

### Responsibilities

- Clean transcripts
- Remove verbal fillers
- Parse regional business jargon
- Identify speakers
- Add timestamps
- Organize conversations chronologically

### Output

A structured transcript that downstream agents can process reliably.

---

## 📋 Agent 2 — Executive Assistant

The Executive Assistant transforms conversations into actions.

### Responsibilities

- Extract Action Items
- Identify Decisions
- Detect Risks
- Assign Task Owners
- Detect Deadlines
- Draft Follow-up Emails
- Generate Meeting Summaries

Through the Google Workspace MCP Server, this agent can also:

- Create Google Docs
- Draft Gmail emails
- Integrate with Workspace tools

---

## 📊 Agent 3 — Efficiency Auditor

MeetIQ doesn't just summarize meetings.

It evaluates them.

The Efficiency Auditor analyzes:

- Speaking time distribution
- Participant engagement
- Decision density
- Meeting duration
- Discussion quality

It then generates an overall **Meeting Efficiency Score**.

Example:

```
Meeting Efficiency Score

78%

✔ Clear ownership

✔ High engagement

⚠ Discussion drifted off-topic for 12 minutes

Recommendation:
This meeting could have been shortened by 20%.
```

---

# 🔗 Google Workspace MCP Integration

MeetIQ uses Google's **Model Context Protocol (MCP)** to securely connect AI agents with Google Workspace.

The Executive Assistant Agent can:

- Draft Gmail emails
- Generate Google Docs
- Access authenticated Workspace resources
- Execute productivity workflows

Authentication is handled using OAuth 2.0, ensuring user data remains secure while leveraging existing Google permissions.

---

# 📚 Core Concepts Demonstrated

| Requirement | Implementation |
|-------------|---------------|
| ✅ Multi-Agent System (ADK) | Three specialized AI agents collaborating |
| ✅ MCP Server | Google Workspace integration |
| ✅ Agent Skills | Transcript parsing, task extraction, efficiency auditing |
| ✅ Security | OAuth 2.0 authentication & credential isolation |
| ✅ Deployability | FastAPI backend + React frontend |

---

# 💻 Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | React + TypeScript + Vite |
| Backend | FastAPI |
| AI Framework | Google Agent Development Kit (ADK) |
| LLM | Google Gemini |
| Tool Integration | Model Context Protocol (MCP) |
| Productivity Tools | Google Docs, Gmail |
| Authentication | OAuth 2.0 |

---

# 📁 Project Structure

```text
MeetIQ/
│
├── agents/                           # AI Agent Layer
│   ├── __init__.py
│   ├── orchestrator.py               # Coordinates the multi-agent workflow
│   ├── scribe.py                     # Cleans & structures meeting transcripts
│   ├── exec_assistant.py             # Extracts action items & automates Workspace tasks
│   ├── auditor.py                    # Calculates meeting efficiency metrics
│   └── workspace_mcp_filter.py       # Google Workspace MCP integration layer
│
├── data/                             # Sample datasets & mock inputs
│   ├── mock_transcript.txt
│   ├── action_items.example.json
│   └── audit_results.example.json
│
├── frontend/                         # React + TypeScript application
│
├── .env.example                      # Environment variable template
├── .gitignore                        # Git ignore rules
└── README.md                         # Project documentation
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.10+
- Node.js 18+

---

## Clone the Repository

```bash
git clone https://github.com/sanvisawant/MeetIQ.git

cd MeetIQ
```

---

## Configure Environment

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

If the Gemini API quota is exceeded, MeetIQ automatically falls back to high-quality mock responses, allowing the application to remain fully functional for demonstrations.

---

# 🔐 Google Workspace Authentication

MeetIQ uses OAuth 2.0 for secure Google Workspace access.

Run:

### PowerShell

```powershell
.\auth_mcp.ps1
```

### Windows CMD

```cmd
auth_mcp.bat
```

Complete the Google sign-in flow.

Credentials are securely stored locally.

---

# ▶ Running MeetIQ

### PowerShell

```powershell
.\start.ps1
```

### Windows CMD

```cmd
start.bat
```

### Unix

```bash
./start.sh
```

Open:

```
http://localhost:8080
```

Upload a meeting transcript to watch the agent pipeline execute in real time.

---

# ⚙ Technical Highlights

## Intelligent Agent Collaboration

MeetIQ separates responsibilities across specialized agents instead of relying on a single monolithic LLM.

This improves:

- Maintainability
- Explainability
- Extensibility

---

## Clever Tool Use

Google Workspace MCP enables agents to interact directly with:

- Gmail
- Google Docs

without manually implementing each Workspace API.

---

## Credential Persistence

OAuth credentials are cached locally inside `.mcp-credentials`, preventing repeated sign-in while maintaining security.

---

## Graceful Failure Handling

If Gemini API limits are exceeded, MeetIQ automatically switches to realistic mock responses, ensuring uninterrupted demonstrations.

---

# 🔒 Security

MeetIQ follows secure development practices.

- OAuth 2.0 Authentication
- Local Credential Storage
- `.gitignore` protection
- No API keys committed
- No OAuth tokens committed
- Principle of Least Privilege

---

# 📸 Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/c6b2d739-ed74-4899-893a-39eb9702b373" width="48%" alt="Efficiency Report"/>
  <img src="https://github.com/user-attachments/assets/da5512be-4f69-46e9-bfcd-200022f7e488" width="48%" alt="Architecture"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/9a1d9168-86bd-4abd-9df3-9149c6c169d8" width="48%" alt="Dashboard"/>
  <img src="https://github.com/user-attachments/assets/a9868183-01a9-4fea-b47e-69314eca101f" width="48%" alt="Transcript Analysis"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/9371d178-e3dc-426b-a8c5-77521c9705c9" width="48%" alt="Google Workspace Integration"/>
  <img src="https://github.com/user-attachments/assets/7a61acec-6403-47cc-ad8f-4b65c6281320" width="48%" alt="MeetIQ Banner"/>
</p>
---

# 🚧 Future Roadmap

- Slack Integration
- Microsoft Teams Integration
- Live Meeting Transcription
- Zoom Integration
- Calendar Automation
- Sentiment Analysis
- Meeting Cost Estimation
- Recurring Meeting Optimization

---

# 🏆 Built for Kaggle

MeetIQ was developed as part of the **Kaggle AI Agents: Intensive Vibe Coding Capstone**.

The project demonstrates:

- Multi-Agent AI Systems
- Google ADK
- MCP Tool Calling
- Enterprise Workflow Automation
- Secure Workspace Integration

---

# 📄 License

This project is intended for educational and demonstration purposes.

---

<div align="center">

## MeetIQ

### Transforming conversations into execution.

</div>
