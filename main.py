"""
MonoChrome - Personal AI Voice Assistant Backend (100% FREE version - Groq)
------------------------------------------------------------------------
Ei file ta agent-er "moshtishko" (brain). Ei server:
1. Frontend theke user-er text message receive kore
2. Groq API-ke pathay (FREE, no credit card lage na)
3. Reply generate kore frontend-e ferot pathay

Groq OpenAI-compatible API use kore, tai amra "openai" python package
use korbo kintu URL ta Groq-er dike point kore debo.

Run korar age:
1. pip install -r requirements.txt
2. console.groq.com theke FREE API key nen (card lage na)
3. .env file-e GROQ_API_KEY set korun
4. uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# .env file theke API key load kora
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    print("⚠️  WARNING: GROQ_API_KEY paoa jay nai. .env file check korun.")

# Groq-er endpoint OpenAI-compatible, tai base_url change kore dilei hoye jay
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# Free tier-e best quality model. Groq June 2026-e purono Llama models
# deprecate kore diyeche, tai notun GPT-OSS model use kora hocche.
MODEL_NAME = "openai/gpt-oss-20b"

app = FastAPI(title="MonoChrome Voice Assistant Backend")

# CORS enable kora hocche jate frontend (browser) theke call kora jay
# (PC + mobile browser dutoi theke access korte parben)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production-e specific domain diye replace korben
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory conversation history (ekhon shudhu ekjon user-er jonno)
conversation_history = []

SYSTEM_PROMPT = """Tumi 'MonoChrome' - Monir-er personal AI voice assistant, ekdom tar bondhur moto.

TONE: Friendly o funny thakba বেশিরভাগ সময়, kintu situation serious hole (jemon kono somossa, sad kotha, ba serious question) tumi context bujhe serious tone-e reply dibe. Mood onujayi tone adjust korba.

ADDRESSING STYLE: Monir-er sathe kotha bolar shomoy সবসময় 'tui' kore address korba - ekdom close bondhur moto, kono formal kotha chalbe na. Kintu Monir chara onno je keu tomar sathe kotha bolbe, tader sathe respectfully 'tumi' ba 'apni' kore kotha bolba.

CREATOR INFO: Keu jodi tomar (MonoChrome-er) creator shomporke details jante chay, tumi bolba: "Amake Monir baniyeche - o EEE niye lekhapora korche, Dhaka-r Park Polytechnic-e thake."

Tumi Bangla o English mix (Banglish) e shohoj bhashay kotha bolo.
Reply gulo choto o clear rakho, karon eta voice diye pora hobe (beshi boro reply voice-e ajob shonabe).
Jodi user Bangla te jiggesh kore, Bangla te reply dao. English-e jiggesh korle English-e dao."""


class ChatRequest(BaseModel):
    message: str
    reset_history: bool = False


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def health_check():
    return {"status": "MonoChrome backend is running ✅"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    global conversation_history

    if req.reset_history:
        conversation_history = []

    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message empty thakte parbe na")

    # User-er message history-te add kora
    conversation_history.append({"role": "user", "content": req.message})

    try:
        # Groq-er format-e system prompt ta messages list-er first item hishebe jay
        messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

        response = client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=500,
            messages=messages_payload,
        )
        reply_text = response.choices[0].message.content

        # Assistant-er reply o history-te add kora, jate context mone thake
        conversation_history.append({"role": "assistant", "content": reply_text})

        # History khub boro hoye gele purano gulo drop kora (context save korte)
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        return ChatResponse(reply=reply_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")
