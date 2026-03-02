
import os

import google.generativeai as genai

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware



# Paste your NEW key here

genai.configure(api_key="AIzaSyA0Ti4dU2Ximt6aFzYc9P2taYyERTE62MM")



app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])



def get_working_model():

    # This lists all models available to your specific key/version

    for m in genai.list_models():

        if 'generateContent' in m.supported_generation_methods:

            return m.name

    return "models/gemini-1.5-flash" # Fallback



WORKING_MODEL = get_working_model()

print(f"--- SYSTEM ONLINE: USING MODEL {WORKING_MODEL} ---")



@app.get("/analyze")

async def analyze(query: str = "test"):

    try:

        model = genai.GenerativeModel(WORKING_MODEL)

        response = model.generate_content(query)

        return {"analysis": response.text}

    except Exception as e:

        return {"analysis": f"Final Bridge Error: {str(e)}"}



@app.get("/")

async def root():

    return {"status": "ALIVE", "model": WORKING_MODEL}

