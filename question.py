from openai import OpenAI
from app.config import GROQ_API_KEY, MODEL_NAME

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def generate_question(role):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a technical interviewer."
            },
            {
                "role": "user",
                "content": f"Ask one interview question for a {role}. Only return the question."
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content