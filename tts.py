import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")


def text_to_speech(text: str):
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=text
    )

    output_path = "output.mp3"

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path