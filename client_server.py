import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.179',65432))

def client(client_socket):

    try:
        while True:
            message = raw_input("Enter message to send to server: ")
            print(message)
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print("Received from server:", data.decode())
    finally:
        client_socket.close()

if __name__ == "__main__":
    client()
