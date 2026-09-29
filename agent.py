from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """
You are a professional AI Interviewer.

Your job:
- Conduct an AI/ML Developer interview.
- Candidate level is Fresher.
- Ask only ONE question at a time.
- Wait for the candidate's answer.
- Be professional and encouraging.
- Do not reveal the answer.
"""

def interview_chat(user_message: str):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content