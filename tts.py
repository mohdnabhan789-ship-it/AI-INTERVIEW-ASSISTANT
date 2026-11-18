from gtts import gTTS
import os
import uuid

def text_to_speech(text: str):
    output_path = os.path.join(
        "temp",
        f"output_{uuid.uuid4().hex}.mp3"
    )

    os.makedirs("temp", exist_ok=True)

    tts = gTTS(
        text=text,
        lang="en",
        slow=False
    )

    tts.save(output_path)

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        raise Exception("TTS audio file was not created.")

    return output_path
