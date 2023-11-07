import socket
from threading import Thread


class Server:
    threads = []

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.stop = False
        self.bind()
        self.is_client = False

    def bind(self):
        print("Création du socket")
        self.s = socket.socket()
        self.s.bind((self.ip, self.port))


    def wait_for_client(self):
        print("Attente d'une connexion d'un client")
        self.s.listen(1)
        self.conn, self.address = self.s.accept()
        print("Nouveau client, connexion effectuée")
        self.is_client = True

    def send_messages(self):
        while not self.stop and self.is_client:
            message = input("Message à envoyer (ou 'arret' pour quitter) : ")
            try:
                self.conn.send(message.encode())
                if message == "bye":
                    print("Fermeture de la connexion avec le client")
                    self.conn.close()
                    self.is_client = False
                    self.wait_for_client()
            except:
                """
                L'autre thread est arrêté donc il faut aussi arrêter celui la
                """
                self.is_client=False
                self.stop = True

    def receive_messages(self):
        while not self.stop and self.is_client:
            try:
                reply = self.conn.recv(1024).decode()
                if reply:
                    print(f"Reçu du client: {reply}")
                if reply == "arret":
                    print("La connexion du serveur et du client s'est bien arrêtée")
                    self.is_client = False
                    self.stop = True
                    self.conn.close()
                    self.s.close()
                if reply == "bye":
                    self.conn.close()
                    self.is_client = False
                    self.wait_for_client()
            except:
                self.stop = True
                self.is_client = False

    def start(self):
        self.wait_for_client()
        self.threads.append(Thread(target=self.send_messages, args=(), name="send"))
        self.threads.append(Thread(target=self.receive_messages, args=(), name="receive"))
        for thread in self.threads:
            thread.start()
        for t in self.threads:
            t.join()

if __name__ == "__main__":
    Server(ip="127.0.0.1", port=6350).start()