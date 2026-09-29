sessions = {}

def get_history(user_id="demo"):
    return sessions.get(user_id, [])

def save_message(user_id, role, content):
    if user_id not in sessions:
        sessions[user_id] = []

    sessions[user_id].append({
        "role": role,
        "content": content
    })