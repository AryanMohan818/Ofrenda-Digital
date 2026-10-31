import os
from pathlib import Path
import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Ofrenda Digital API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
GEMMA_MODEL = os.getenv("GEMMA_MODEL", "gemma2:2b")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM") # Rachel / warm default

class MemorialRequest(BaseModel):
    name: str
    relation: Optional[str] = "Loved One"
    years: Optional[str] = ""
    favorite_memories: str
    favorite_foods: Optional[str] = ""
    favorite_music: Optional[str] = ""

@app.get("/api/health")
def health_check():
    return {"status": "ok", "model": GEMMA_MODEL, "ollama_host": OLLAMA_HOST}

@app.post("/api/remember")
def generate_remembrance(memorial: MemorialRequest):
    """
    Invokes the local Gemma open-weight model to compose an ofrenda eulogy and oral history.
    """
    system_prompt = (
        "You are an empathetic chronicler and guardian of memories for Día de los Muertos (Day of the Dead). "
        "Your duty is to honor the spirits of those who have crossed over with poetic warmth, deep reverence, "
        "and vivid sensory details of marigolds (cempasúchil), candlelight, and cherished memories. "
        "Write a heartfelt 3-paragraph remembrance eulogy and blessing for this loved one."
    )

    user_prompt = f"""
Honoring: {memorial.name} ({memorial.relation})
Life Years: {memorial.years if memorial.years else 'Remembered Eternally'}
Cherished Memories & Traits: {memorial.favorite_memories}
Favorite Foods / Treats for the Altar: {memorial.favorite_foods if memorial.favorite_foods else 'Pan de Muerto, sweet fruit, and fresh water'}
Favorite Music & Melodies: {memorial.favorite_music if memorial.favorite_music else 'Gentle acoustic strings and laughter'}

Please compose an ofrenda blessing and poetic remembrance honoring their spirit. Keep the tone loving, celebratory, and comforting.
"""

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": GEMMA_MODEL,
                "prompt": f"{system_prompt}\n\n{user_prompt}",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            },
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            return {"remembrance": result.get("response", "").strip()}
        else:
            raise HTTPException(status_code=500, detail=f"Ollama error: {response.text}")
    except requests.exceptions.RequestException as e:
        # Graceful fallback if Ollama container is starting or offline
        fallback_text = (
            f"Candles glow tonight for {memorial.name}, our beloved {memorial.relation}. "
            f"The petals of cempasúchil guide your steps back home to us. "
            f"We set the table with your favorites—{memorial.favorite_foods or 'pan de muerto and sweets'}—"
            f"and let the melodies you loved ({memorial.favorite_music or 'songs of joy'}) fill the evening air. "
            f"You are never truly gone as long as we hold your memories alive: {memorial.favorite_memories}. "
            f"May your spirit rest in light, peace, and eternal love."
        )
        return {"remembrance": fallback_text, "note": f"Local inference connecting... (Error: {str(e)})"}

@app.post("/api/tts")
def voice_remembrance(text: str):
    """
    Optional: Uses ElevenLabs if API key is provided, or returns instructions to use Web Speech API.
    """
    if not ELEVENLABS_API_KEY:
        return {"audio_url": None, "use_browser_speech": True}

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        res = requests.post(url, json=data, headers=headers)
        if res.status_code == 200:
            import base64
            b64_audio = base64.b64encode(res.content).decode("utf-8")
            return {"audio_base64": f"data:audio/mp3;base64,{b64_audio}", "use_browser_speech": False}
        else:
            return {"audio_url": None, "use_browser_speech": True}
    except Exception:
        return {"audio_url": None, "use_browser_speech": True}

# Resolve the frontend directory whether running locally or inside Docker
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = Path("/app/frontend")

app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")