import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai
from google.genai import types

from .identity import CYBERSHIELD_PROMPT

load_dotenv()
api_key = os.getenv("CYBERSHIELD_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()
templates = Jinja2Templates(directory="backend/templates")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

WORKING_MODEL = "gemini-3-flash-preview"

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "agent": 'CyberShield AI "El Guardian!🛡️"',
        "mission": "FIFA World Cup 2026 Protection",
        "status": "ACTIVE"
    })

@app.get("/analyze")
async def analyze(query: str = "test"):
    try:
        response = client.models.generate_content(
            model=WORKING_MODEL,
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=CYBERSHIELD_PROMPT
            )
        )
        return {"analysis": response.text}
    except Exception as e:
        return {"analysis": f"Shield Error: {str(e)}"}

print(f'--- SYSTEM ONLINE: CyberShield AI "El Guardian!🛡️" ACTIVATED ---')