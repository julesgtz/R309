import socket
from threading import Thread


class Connexion:
    threads = []

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.stop = False
        self.connect()

    def connect(self):
        self.s = socket.socket()
        self.s.connect((self.ip, self.port))
        print("Succesfully connected")

    def send_messages(self):
        while not self.stop:
            message = input("Message à envoyer (ou 'arret' pour quitter) : ")
            self.s.send(message.encode())
            if message == "bye":
                print("Fermeture de la connexion")
                self.s.close()
                login = input("Voulez vous vous reconnecter ?")
                if login:
                    self.connect()

    def receive_messages(self):
        while not self.stop:
            reply = self.s.recv(1024).decode()
            if reply:
                print(f"Reçu du serveur: {reply}")
            if reply == "arret":
                print("La connexion du serveur et du client s'est bien arrêtée")
                self.s.close()

    def start(self):
        self.threads.append(Thread(target=self.send_messages, args=()))
        self.threads.append(Thread(target=self.receive_messages, args=()))
        for thread in self.threads:
            thread.start()
        for t in self.threads:
            t.join()


if __name__ == "__main__":
    Connexion(ip="10.128.4.44", port=6350).start()
    # Connexion(ip="10.128.4.42", port=6250).start()
