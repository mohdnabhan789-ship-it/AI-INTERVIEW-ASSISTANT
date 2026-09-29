from app.question import generate_question
from app.agent import interview_feedback

# Temporary memory
sessions = {}

def start_interview(name, role):
    question = generate_question(role)

    sessions[name] = {
        "role": role,
        "question": question
    }

    return question


def submit_answer(name, answer):
    data = sessions[name]

    feedback = interview_feedback(
        data["role"],
        answer
    )

    next_question = generate_question(data["role"])

    sessions[name]["question"] = next_question

    return feedback, next_question