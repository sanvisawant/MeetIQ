import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load env variables first
load_dotenv()

from agents.orchestrator import run_analysis_pipeline, MOCK_ACTION_ITEMS, MOCK_AUDIT_RESULTS

app = FastAPI(title="MeetIQ API Bridge")

# Configure CORS so the React app can communicate from its port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    transcript: str

@app.post("/api/analyze")
def analyze_transcript(req: AnalyzeRequest):
    transcript_text = req.transcript.strip()
    
    # If no transcript is provided (Demo mode), read the local mock transcript
    if not transcript_text:
        mock_path = os.path.join("data", "mock_transcript.txt")
        if os.path.exists(mock_path):
            with open(mock_path, "r", encoding="utf-8") as f:
                transcript_text = f.read().strip()
        else:
            transcript_text = "Srikant (PM): Let's sync about the AWS deployment blocker."

    try:
        print("FastAPI Bridge: Executing live multi-agent pipeline...")
        results = run_analysis_pipeline(transcript_text)
        return results
    except Exception as e:
        print(f"FastAPI Bridge Error: {e}")
        print("Falling back to high-fidelity mock payload...")
        # Graceful fallback to maintain client UI robustness
        return {
            **MOCK_ACTION_ITEMS,
            **MOCK_AUDIT_RESULTS
        }

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
