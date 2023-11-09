import socket
from threading import Thread


class Server:
    threads = []
    d_client = {}

    def __init__(self, max_user: int, ip: str, port: int):
        self.m = max_user
        self.c = 0
        self.ip = ip
        self.port = port
        self.bind()

    def bind(self):
        print("Création du socket")
        self.s = socket.socket()
        self.s.bind((self.ip, self.port))

    def accept_clients(self):
        self.c += 1
        while self.m >= self.c:
            client, address = self.s.accept()
            print(f"Nouvelle connexion : {address[0]}")
            thread = Thread(target=self.client_hdl, args=(self, client))
            self.threads.append(thread)
        else:
            print("Max users sur le serveur")

    def client_hdl(self, new_client):
        new_client.send(str.encode("Tu es actuellement connecté au serveur relais"))
        connected = True
        while connected:
            reply = new_client.recv(1024).decode()
            if reply == 'bye':
                connected = False
            new_client.sendall(str.encode(reply))
        else:
            new_client.close()
            self.c -= 1

    def start(self):
        while True:
            self.accept_clients()

