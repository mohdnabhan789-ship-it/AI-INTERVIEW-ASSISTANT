
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

import shutil
import os
import time
import uuid
from datetime import datetime

from app.stt import speech_to_text
from app.agent import interview_chat
from app.tts import text_to_speech


# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI(title="AI Voice Interview Assistant")


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# TEMP DIRECTORY
# =========================================================

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


# =========================================================
# HOME ENDPOINT
# =========================================================

@app.get("/")
def home():
    return {
        "message": "AI Voice Interview Assistant Running"
    }


# =========================================================
# AUDIT LOGGER
# =========================================================

def audit_log(
    action,
    function,
    tool,
    status,
    latency,
    error=None
):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n----------------------------------------")
    print(f"Time      : {timestamp}")
    print(f"Action    : {action}")
    print(f"Function  : {function}")
    print(f"Tool      : {tool}")
    print(f"Status    : {status}")
    print(f"Latency   : {latency:.2f} seconds")

    if error:
        print(f"Error     : {error}")

    print("----------------------------------------")


# =========================================================
# VOICE INTERVIEW ENDPOINT
# =========================================================

@app.post("/voice-interview")
async def voice_interview(file: UploadFile = File(...)):

    total_start = time.perf_counter()

    input_audio = os.path.join(
        TEMP_DIR,
        f"recording_{uuid.uuid4().hex}.webm"
    )

    output_audio = None

    try:

        # STEP 1: SAVE AUDIO

        upload_start = time.perf_counter()

        with open(input_audio, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        upload_time = time.perf_counter() - upload_start

        audit_log(
            action="Save Audio",
            function="shutil.copyfileobj()",
            tool="Python File System",
            status="SUCCESS",
            latency=upload_time
        )

        # STEP 2: SPEECH TO TEXT

        stt_start = time.perf_counter()

        user_text = speech_to_text(input_audio)

        stt_time = time.perf_counter() - stt_start

        audit_log(
            action="Speech to Text",
            function="speech_to_text()",
            tool="Groq Whisper",
            status="SUCCESS",
            latency=stt_time
        )

        # STEP 3: TEXT TO AI

        llm_start = time.perf_counter()

        ai_text = interview_chat(user_text)

        llm_time = time.perf_counter() - llm_start

        audit_log(
            action="Generate AI Response",
            function="interview_chat()",
            tool="Groq LLM",
            status="SUCCESS",
            latency=llm_time
        )

        # STEP 4: AI TEXT TO VOICE

        tts_start = time.perf_counter()

        output_audio = text_to_speech(ai_text)

        tts_time = time.perf_counter() - tts_start

        audit_log(
            action="Text to Speech",
            function="text_to_speech()",
            tool="Google gTTS",
            status="SUCCESS",
            latency=tts_time
        )

        # TOTAL TIME

        total_time = time.perf_counter() - total_start

        print("\n============================================")
        print("        AI INTERVIEW AUDIT SUMMARY")
        print("============================================")

        print(f"User Text     : {user_text}")
        print(f"AI Response   : {ai_text}")

        print("--------------------------------------------")

        print(f"Audio Upload  : {upload_time:.2f} sec")
        print(f"STT           : {stt_time:.2f} sec")
        print(f"LLM           : {llm_time:.2f} sec")
        print(f"TTS           : {tts_time:.2f} sec")

        print("--------------------------------------------")

        print(f"TOTAL TIME    : {total_time:.2f} sec")

        print("============================================")

        # RETURN AUDIO AND DELETE AFTER RESPONSE

        return FileResponse(
            path=output_audio,
            media_type="audio/mpeg",
            filename="ai_reply.mp3",
            background=BackgroundTask(os.remove, output_audio)
        )

    except Exception as e:

        print("\nVOICE INTERVIEW FAILED:", str(e))

        if output_audio and os.path.exists(output_audio):
            os.remove(output_audio)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if os.path.exists(input_audio):
            os.remove(input_audio)

        await file.close()
