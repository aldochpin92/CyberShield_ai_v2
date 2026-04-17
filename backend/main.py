import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from google import genai
from google.genai import types

# Import the refined Identity Spine
from .identity import CYBERSHIELD_PROMPT, GUARDIAN_SIGNATURE 

load_dotenv()
api_key = os.getenv("CYBERSHIELD_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()
templates = Jinja2Templates(directory="backend/templates")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

WORKING_MODEL = "gemini-3-flash-preview"

class AnalyzeRequest(BaseModel):
    query: str
    mission: str = "home_base" # Default to Home Base [cite: 2, 64]

# --- PHASE II CORE ROUTER [cite: 7, 156, 157] ---
def route_request(query: str):
    """
    Core Router logic to identify which agent handles the request.
    """
    query_lower = query.lower()
    if any(word in query_lower for word in ["scam", "profile", "fake", "dating"]):
        return "Anti-Scammer Goalie" [cite: 3, 82]
    elif any(word in query_lower for word in ["data", "compliance", "gdpr", "law"]):
        return "Sideline Referee" [cite: 3, 83]
    elif any(word in query_lower for word in ["video", "deepfake", "audio", "image"]):
        return "Red Card Sentinel" [cite: 3, 84]
    elif any(word in query_lower for word in ["ddos", "log", "stadium", "attack"]):
        return "Las Barras Bravas Triage" [cite: 3, 85]
    return "El Guardián Core" [cite: 5, 124]

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "agent": 'CyberShield AI "El Guardián"',
        "signature": GUARDIAN_SIGNATURE, #
        "mission": "FIFA World Cup 2026 Protection", #
        "status": "ACTIVE"
    })

@app.post("/analyze")
async def analyze(payload: AnalyzeRequest):
    query = payload.query.strip()
    
    if not query:
        return {"analysis": "Please provide data for El Guardián to inspect."}

    # Identify the active agent for this request
    active_agent = route_request(query)

    try:
        # Use Behavioral Rules for the response
        response = client.models.generate_content(
            model=WORKING_MODEL,
            contents=f"Agent Context: {active_agent}\nUser Query: {query}",
            config=types.GenerateContentConfig(
                system_instruction=CYBERSHIELD_PROMPT
            )
        )
        return {
            "agent": active_agent,
            "analysis": response.text,
            "signature": GUARDIAN_SIGNATURE #
        }
    except Exception as e:
        return {"analysis": f"Shield Error: {str(e)}"}

print(f'--- SYSTEM ONLINE: {GUARDIAN_SIGNATURE} ACTIVATED ---')