import socket

def server(server_socket):

    print("Server is waiting for a connection")
    conn, addr = server_socket.accept()
    print("Connected by", addr)
    all_data = []
    
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Received from client:", data)
        all_data.append(data.decode('utf-8'))
        conn.sendall(b"Server received: " + data)

    conn.close()

if __name__ == "__main__":
    server()
