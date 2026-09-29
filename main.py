from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os

from app.stt import speech_to_text
from app.agent import interview_chat
from app.tts import text_to_speech

app = FastAPI(title="AI Voice Interview Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Voice Interview Assistant Running"}


@app.post("/voice-interview")
async def voice_interview(file: UploadFile = File(...)):

    # Save microphone recording
    input_audio = "recording.webm"

    with open(input_audio, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # STEP 1 : Speech → Text
    user_text = speech_to_text(input_audio)

    # STEP 2 : Text → AI
    ai_text = interview_chat(user_text)

    # STEP 3 : AI Text → Voice
    output_audio = text_to_speech(ai_text)

    # Delete temporary recording
    if os.path.exists(input_audio):
        os.remove(input_audio)

    # Return AI voice
    return FileResponse(
        path=output_audio,
        media_type="audio/mpeg",
        filename="ai_reply.mp3"
    )