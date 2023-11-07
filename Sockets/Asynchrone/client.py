import socket
from threading import Thread

class Connexion:
    threads = []

    def __init__(self, ip: str, port: int):
        self.s = socket.socket()
        self.s.connect((ip, port))

    def send_messages(self):
        while True:
            message = input("Message à envoyer (ou 'arret' pour quitter) : ")
            self.s.send(message.encode())
            if message == "arret":
                print("Fermeture de la connexion")
                self.s.close()

    def receive_messages(self):
        while True:
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
    # Connexion(ip="10.128.4.44", port=6350).start()
    Connexion(ip="10.128.4.44", port=6350).start()