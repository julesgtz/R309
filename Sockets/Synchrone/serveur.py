import socket

server_socket = socket.socket()
server_socket.bind(("127.0.0.1", 6350))
server_socket.listen(1)
conn, address = server_socket.accept()

while True:
    message = conn.recv(1024).decode()
    print(message)
    reply = input("REPLY : ")
    conn.send(reply.encode())

    if message == "arret":
        conn.close()
        server_socket.close()
        break