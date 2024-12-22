import json

def load_session_data(uploaded_files):
    sessions = []
    for file in uploaded_files:
        content = file.read()
        if file.name.endswith(".txt"):
            content = json.loads(content.decode("utf-8"))  # Parse TXT as JSON
        else:
            content = json.load(file)  # Parse JSON directly
        sessions.append(content)
    return sessions