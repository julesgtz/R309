import socket

client_socket = socket.socket()
connected = False
while True:
    if not connected:
        message = input("Tapes 'entrée' pour te connecter ")
        client_socket.connect(("127.0.0.1", 6350))
    connected = True
    message = input("message : ")
    client_socket.send(message.encode())
    reply = client_socket.recv(1024).decode()
    print(reply)

    if message == "bye":
        client_socket.close()
        connected = False

