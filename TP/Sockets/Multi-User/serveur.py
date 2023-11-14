import socket
from threading import Thread


class Server:
    d_client = {}

    def __init__(self, max_user: int, ip: str, port: int):
        global c_user
        c_user = 0
        self.m = max_user
        self.ip = ip
        self.port = port
        self.bind()
        self.running = True

    def bind(self):
        print("Création du socket")
        self.s = socket.socket()
        self.s.bind((self.ip, self.port))

    def accept_clients(self):
        global c_user
        while self.running:
            while self.m >= c_user:
                client, address = self.s.accept()
                print(f"Nouvelle connexion : {address[0]}")
                thread = Thread(target=self.client_hdl, args=(self, client, address[0]))
                c_user += 1
                thread.start()
                thread.join()
            else:
                print("Max users sur le serveur, attente qu'une place se libère")

    def client_hdl(self, new_client, ip):
        global c_user
        new_client.send(str.encode("Tu es actuellement connecté au serveur relais"))
        connected = True
        while connected:
            reply = new_client.recv(1024).decode()
            if reply == 'bye':
                connected = False
            new_client.sendall(str.encode(f"{reply}, ip : {ip}"))
        else:
            new_client.close()
            c_user -= 1

    def start(self):
        while self.running:
            self.accept_clients()

if __name__ == "__main__":
    Server(ip="127.0.0.1", port=6350, max_user=1).start()

