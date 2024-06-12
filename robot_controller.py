# -*- coding: utf-8 -*-
import qi
import sys
import socket



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.179',65432))
server_socket.listen(1)

topics = ["Where", "When", "Who", "Other"]

questions = {
    "Who": ["Who is in the photo?", "Can you tell me more about the people in the photo?", "Who else was there?"],
    "Where": ["Where was this photo taken?", "What can you tell me about this place?", "Is this place special to you?"],
    "When": ["When was this photo taken?", "What time of the year was it?", "How old were you when this photo was "
                                                                            "taken?"],
    "Other": ["Is there anything else you can tell me about this photo?", "What memories does this photo bring back?",
              "Why is this photo important to you?"]
}

current_topic_index = 0
current_question_index = 0
question_count = 0

def get_next_question():
    global current_topic_index, current_question_index
    if current_topic_index < len(topics):
        topic = topics[current_topic_index]
        if current_question_index < len(questions[topic]):
            question = questions[topic][current_question_index]
            current_question_index += 1
            return question
        else:
            current_question_index = 0
            current_topic_index += 1
            return get_next_question()
    else:
        return "Thank you for sharing the information about the photo!"
        

def extract_feedback(conversation_string):
    feedback = ""
    for line in conversation_string.split('\n'):
        if "feedback:" in line:
            feedback = line.split("feedback:")[1].strip()
            break
    return feedback

def main():
    # 设置机器人 IP 和端口
    robot_ip = "192.168.1.91"  # 替换为你的机器人 IP 地址
    robot_port = 9559  # 替换为你的机器人端口号

    # 创建 session 并连接到机器人
    session = qi.Session()
    try:
        session.connect("tcp://" + robot_ip + ":" + str(robot_port))
        print("Connected to the robot at", robot_ip)
    except :
        print("Can't connect to Naoqi at ip \"" + robot_ip + "\" on port " + str(robot_port) + ".\nPlease check your script arguments. Run with -h option for help.")
        sys.exit(1)
        
	# using ALTextSpeech service
    tts = session.service("ALTextToSpeech")
    
	# let the robot talks
    tts.say("Hello, I am a Nao robot. How can I assist you today?")
    conn, addr = server_socket.accept()

    try:
        conn, addr = server_socket.accept()
        print("Connected by", addr)
        initial_prompt = get_next_question()
        conn.sendall(initial_prompt.encode('utf-8'))
        tts.say(initial_prompt)
    except Exception as e:
        print(f"Failed to accept connection: {e}")
        sys.exit(1)  # Exit the main function


    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Received from client:", data)
        feedback = extract_feedback(data)
        tts.say(str(feedback))
        next_prompt = get_next_question()
        tts.say(next_prompt)
        conn.sendall(next_prompt.encode('utf-8'))

    conn.close()


if __name__ == "__main__":
    main()
