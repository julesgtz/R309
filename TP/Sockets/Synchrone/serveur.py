import socket

server_socket = socket.socket()
server_socket.bind(("10.128.4.44", 6350))
server_socket.listen(1)
conn, address = server_socket.accept()
print("Succesfully connected")
while True:
    message = conn.recv(1024).decode()
    print(f"Vous avez recu un nouveau message : {message}")

    if message == "arret":
        print("La connexion du serveur et du client s'est bien arrêtée")
        conn.close()
        server_socket.close()
        break

    elif message == "bye":
        conn.close()
        print("Attente d'une nouvelle connexion")
        server_socket.listen(1)
        conn, address = server_socket.accept()
        print("Succesfully connected")

    else:
        reply = input("Veuillez inserer une réponse : ")
        conn.send(reply.encode())
