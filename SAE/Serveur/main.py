import socket
from threading import Thread
from time import sleep


class Server:
    def __init__(self, max_user: int, ip: str, port: int):
        global c_user, conn_client
        conn_client = []
        c_user = 0
        self.m = max_user
        self.ip = ip
        self.port = port
        self.__bind()
        self.running = True

    def __bind(self):
        print("Création du socket")
        self.s = socket.socket()
        self.s.bind((self.ip, self.port))

    def __accept_clients(self):
        global c_user, conn_client
        while self.running:
            while self.m > c_user:
                print("Attente d'un client")
                self.s.listen(self.m)
                client, address = self.s.accept()
                print(f"Nouvelle connexion : {address[0]}")
                conn_client.append(client)
                thread = Thread(target=self.client_hdl, args=(client, address[0]))
                c_user += 1
                thread.start()
            else:
                print("Max users sur le serveur, attente qu'une place se libère ~30s")
                sleep(30)

    def __send_all(self, conn, msg):
        global conn_client
        for con in conn_client:
            if con != conn:
                con.send(msg.encode())


    def client_hdl(self, new_client, ip):
        global c_user
        global conn_client
        new_client.send(str.encode("Tu es actuellement connecté au serveur relais"))
        connected = True
        while connected:
            reply = new_client.recv(1024).decode()
            if reply == 'bye':
                connected = False
            self.__send_all(conn=new_client, msg=f"{reply}, ip : {ip}")
        else:
            new_client.close()
            conn_client.remove(new_client)
            c_user -= 1

    def start(self):
        while self.running:
            self.__accept_clients()

if __name__ == "__main__":
    Server(ip="127.0.0.1", port=6350, max_user=2).start()

