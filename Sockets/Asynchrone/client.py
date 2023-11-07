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
        self.stop = False
        print("Succesfully connected")

    def send_messages(self):
        while not self.stop:
            message = input("Message à envoyer ('bye' ou 'arret' pour quitter) : ")
            self.s.send(message.encode())
            if message == "bye":
                self.stop = True
                print("Fermeture de la connexion")
                self.s.close()
            if message=="arret":
                self.s.close()
                self.stop = True

    def receive_messages(self):
        while not self.stop:
            try:
                reply = self.s.recv(1024).decode()
                if reply:
                    print(f"Reçu du serveur: {reply}")
                if reply == "arret":
                    print("La connexion du serveur et du client s'est bien arrêtée")
                    self.s.close()
                    self.stop = True
            except:
                """
                la connexion avec le serveur a été arreté, donc il faut stop ce thread
                """
                self.stop=True
    def start(self):
        self.threads.append(Thread(target=self.send_messages, args=()))
        self.threads.append(Thread(target=self.receive_messages, args=()))
        for thread in self.threads:
            thread.start()

        for t in self.threads:
            t.join()


if __name__ == "__main__":
    Connexion(ip="127.0.0.1", port=6350).start()
    # Connexion(ip="10.128.4.42", port=6250).start()
