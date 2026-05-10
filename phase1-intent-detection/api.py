from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from router import process_message

app = FastAPI(
    title="LeadMind API",
    description="AI-powered lead intent detection and auto-reply generation.",
    version="1.0.0"
)


# ── Request / Response models ─────────────────────────────────────────────────

class IncomingMessage(BaseModel):
    message: str
    lead_name: Optional[str] = "there"
    lead_company: Optional[str] = ""
    rep_name: Optional[str] = "Alex"
    company_context: Optional[str] = ""


class ProcessedResponse(BaseModel):
    intent: str
    confidence: float
    sentiment: str
    urgency: str
    action: str
    reply: Optional[str]
    key_signals: List[str]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "LeadMind API is running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/process-message", response_model=ProcessedResponse)
def handle_message(payload: IncomingMessage):
    """
    Process an incoming lead message:
    - Classify intent
    - Route to appropriate action
    - Generate a personalized reply
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    lead = {
        "name": payload.lead_name,
        "company": payload.lead_company,
        "rep_name": payload.rep_name,
        "company_context": payload.company_context
    }

    try:
        result = process_message(payload.message, lead)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

    return result


# ── Run ───────────────────────────────────────────────────────────────────────
# uvicorn api:app --reload
