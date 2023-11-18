import socket
from threading import Thread
from time import sleep
import argparse
import ipaddress


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
        print(f"Running sur l'ip {self.ip}:{self.port}, {self.m} max users")

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

def args_checker(args):
    try:
        ipaddress.ip_address(args.get("i", None))
    except ValueError:
        print("L'ip que vous avez selectionné n'est pas bonne")
        return False
    except Exception as e:
        print(e)
        return False

    try:
        port = args.get("p",None)
        assert 0<port<65535
    except AssertionError:
        print("Le port n'est pas compris entre 0 et 65535")
        return False
    except Exception as e:
        print(e)
        return False

    try:
        users = args.get("u",None)
        assert 0<users<100
    except AssertionError:
        print("Le nombre d'users max n'est pas entre 0 et 100")
        return False
    except Exception as e:
        print(e)
        return False

    return True



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Selectionne l'ip avec -i , le port avec -p , et le nombre max d'user avec -u")
    parser.add_argument('-i', required=True, type=str,
                        help="L'ip du serveur")
    parser.add_argument('-p', required=True, type=int,
                        help='Le port du server')
    parser.add_argument('-u', required=True, type=int,
                        help="Le nombre max d'users")

    args = vars(parser.parse_args())
    is_args_good = args_checker(args)

    if is_args_good:
        Server(ip=args['i'], port=args['p'], max_user=args['u']).start()

