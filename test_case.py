def extract_feedback(conversation_string):
    feedback = ""
    for line in conversation_string.split('\n'):
        if "feedback:" in line:
            feedback = line.split("feedback:")[1].strip()
            break
    return feedback



extract_feedback()