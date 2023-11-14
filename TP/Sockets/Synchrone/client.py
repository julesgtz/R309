import socket

connected = False
while True:
    if not connected:
        client_socket = socket.socket()
        message = input("Tapes 'entrée' pour te connecter ")
        client_socket.connect(("127.0.0.1", 6350))
    connected = True
    message = input("message : ")
    client_socket.send(message.encode())
    reply = client_socket.recv(1024).decode()
    if reply:
        print(f"Le serveur vous a envoyé le message suivant : {reply}")

    if message == "bye":
        print("Fermeture de la connexion")
        client_socket.close()
        connected = False

    if reply == "arret":
        print("La connexion du serveur et du client s'est bien arrêtée")
        client_socket.close()

