from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def speech_to_text(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            response_format="verbose_json"
        )

    return transcription.text