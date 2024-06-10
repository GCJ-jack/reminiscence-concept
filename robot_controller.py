# -*- coding: utf-8 -*-
import qi
import sys
import socket_conection as server_module
import socket



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.179',65432))
server_socket.listen(1)

def main():
    # 设置机器人 IP 和端口
    robot_ip = "192.168.1.91"  # 替换为你的机器人 IP 地址
    robot_port = 9559  # 替换为你的机器人端口号

    # 创建 session 并连接到机器人
    session = qi.Session()
    try:
        session.connect("tcp://" + robot_ip + ":" + str(robot_port))
        print("Connected to the robot at", robot_ip)
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + robot_ip + "\" on port " + str(robot_port) + ".\nPlease check your script arguments. Run with -h option for help.")
        sys.exit(1)
        
	# using ALTextSpeech service
    tts = session.service("ALTextToSpeech")
    
	# let the robot talks
    tts.say("Hello, I am a Nao robot. How can I assist you today?")
    data = server_module.server(server_socket)
    # extract tge feedback part
    feedback = ""
    for line in data:
        if "feedback:" in line:
            feedback = line.split("feedback:")[1].strip()
            break
    # check and say the feedback
    
    if feedback:
        tts.say(feedback)
    else:
        tts.say("I didn't receive any feedback in the data.")


if __name__ == "__main__":
    main()
