import socket
from threading import Thread, current_thread, Event
from time import sleep
from helper import *
import json
import ipaddress
import os
import re
import sys
# des qu'on accepte une demande de join de channels, envoyer un msg au client
# des qu'un user se log, il veut savoir sur quels channels il a acces


class Server:
    def __init__(self, max_user: int, ip: str, port: int, ip_bdd: str):
        """
        Initialisation de la classe server

        :param max_user: Le nombre max d'users sur le serveur
        :param ip: l'ip du serveur
        :param port: le port du serveur
        :param ip_bdd: l'ip de la base de données
        """
        self.user_conn = {}
        self.conn_client = []
        self.user_status = {}
        # user : status (idle / connected)
        self.c_user = 0
        self.m = max_user
        self.ip = ip
        self.port = port
        self.running = True
        self.threads = []
        self.connexion = None
        self.exit_flag = Event()

        self.ip_bdd = ip_bdd



    def __channel_rq(self):
        """
        Permet au server d'accepter / refuser les requêtes pour rejoindre un channel
        """
        # doit faire en sorte que de se log sur admin, ne pas proposé un username mais seulement un mdp
        logged= False

        username, password_to_find = get_user_pwd("admin", connexion=self.connexion)

        while not logged and self.running and not self.exit_flag.is_set():
            print("Vous devez vous log pour pouvoir Accepter / refuser des demandes pour rejoindre des channels")
            print("Username : admin")
            password = str(input("Password : "))

            os.system('cls' if os.name == 'nt' else 'clear')

            if re.match(r'^[A-Za-z\d@$!%*?&]*$', password):
                if password == password_to_find:
                    logged = True
                    print("Vous êtes log !")
                else:
                    print("Mauvais mot de passe \n")
            else:
                print("Le mot de passe ne correspond pas aux critères, réessayez \n")



        while self.running and not self.exit_flag.is_set():
            need_refresh = False

            need_accept = get_channel_rq(connexion=self.connexion)

            os.system('cls' if os.name == 'nt' else 'clear')
            print("Voici les demandes :")
            c_rq = 0

            if need_accept:
                for rq in need_accept:
                    c_rq += 1
                    request_id ,channel_name, user_name = rq
                    print(f"{c_rq} : Demande de {user_name} pour rejoindre le channel {channel_name}")
                print("\n")
                reponse_id = None

                while not reponse_id and not self.exit_flag.is_set():
                    reponse_id = input("Entrez le numéro de requête que vous voulez gérer (R / r pour refresh // C / c pour faire des commandes) : ")
                    try:
                        reponse_id = int(reponse_id)
                        if not 0< reponse_id < c_rq:
                            print(f"La requête {reponse_id} n'existe pas")
                            reponse_id = None

                    except:
                        try:
                            reponse_id = str(reponse_id).lower()
                            if not reponse_id == "r" or not reponse_id == "c":
                                print(f"Tapez (R / r pour refresh // C / c pour faire des commandes), {reponse_id} n'existe pas")
                                reponse_id = None
                            else:
                                if reponse_id == "c":
                                    exit = False
                                    while not exit and not self.exit_flag.is_set():
                                        command = input("""
                                        Commandes de la forme : 'commande (kick/ban)' 'user/ip' 'kick_time (en heures)'
                                        \n
                                        Exemples de commandes : 
                                        \n kick jules 24 (pour kick jules pendant 24heures)
                                        \n ban jules (pour bannir jules)
                                        \n ban 192.168.1.1 (pour bannir l'ip 192.168.1.1)
                                        \n kick 192.168.1.1 12 (pour kick l''ip 192.168.1.1 pendant 12 heures)
                                        \n
                                        \nEntrez la commande que vous voulez (Q / q pour quitter): """).split(" ")
                                        try:
                                            if len(command) == 1 and str(command[0]).lower() == "q":
                                                exit = True
                                            elif len(command) == 2:
                                                if str(command[0]).lower() == "ban":
                                                    user = str(command[1]).lower()
                                                    try:
                                                        ipaddress.ip_address(user)
                                                        good = ban_user(ip=user, connexion=self.connexion)
                                                        if good:
                                                            print(f"L'ip {user} a bien été banni")
                                                        else:
                                                            print(f"L'ip {user} n'existe pas")

                                                    except:
                                                        good = ban_user(ip=user, connexion=self.connexion)
                                                        if good:
                                                            print(f"L'{user} a bien été banni")
                                                        else:
                                                            print(f"L'{user} n'existe pas")


                                            elif len(command) == 3:
                                                user = str(command[1]).lower()
                                                try:
                                                    ipaddress.ip_address(user)
                                                    good, date = kick_user(ip=user,
                                                                           duree=int(command[2]),
                                                                           connexion=self.connexion)
                                                    if good:
                                                        print(f"L'ip {user} kick jusqu'au {date}")
                                                    else:
                                                        print(f"L'ip {user} n'existe pas")
                                                except:
                                                    good, date = kick_user(ip=user,
                                                                           duree=int(command[2]),
                                                                           connexion=self.connexion)
                                                    if good:
                                                        print(f"L'{user} kick jusqu'au {date}")
                                                    else:
                                                        print(f"L'{user} n'existe pas")
                                            else:
                                                pass
                                        except:
                                            pass
                                else:
                                    need_refresh = True
                        except:
                            reponse_id = None

                if not need_refresh:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"Vous avez séléctionné la requête numéro {reponse_id}")
                    request_id, channel_name, user_name = need_accept[reponse_id]
                    print(f"Demande de {user_name} pour rejoindre le channel {channel_name}")

                    reponse = None
                    while not reponse and not self.exit_flag.is_set():
                        try:
                            reponse = str(input("Voulez vous accepter / refuser la requête (exit/quit pour quitter, a/accepter pour accepter, r/refuser pour refuser) : "))
                            if reponse.lower() == 'exit' or 'quit':
                                reponse = True
                            elif reponse.lower() == 'a' or 'accepter':
                                set_status_channel_rq(connexion=self.connexion, accept=True, request_id=request_id)
                                self.user_conn[user_name].send(str.encode(json.dumps({'join': True, "channel_name":channel_name, "status":"accept"})))

                            elif reponse.lower() == 'r' or 'refuser':
                                set_status_channel_rq(connexion=self.connexion, refuse=True, request_id=request_id)
                                self.user_conn[user_name].send(str.encode(json.dumps({'join': True, "channel_name":channel_name, "status":"refuse"})))

                            else:
                                print(f"{reponse} n'existe pas")
                                reponse = None
                        except:
                            reponse = None
                print("Actualisation dans 10s")
                sleep(10)
            else:
                print("Actualisation dans 10s, pas de nouvelles demandes")
                sleep(10)
        else:
            self.threads.remove(current_thread())

    def __bind(self):
        """
        Permet de créer le socket et de bind l'ip et le port au socket

        :return: :bool: Si la connexion est réussie
        """
        try:
            print("Création du socket")
            self.s = socket.socket()
            self.s.bind((self.ip, self.port))
            print(f"Running sur l'ip {self.ip}:{self.port}, {self.m} max users")
        except socket.error as e:
            print(f"Erreur lors de la liaison du socket : {e}")
            return False
        else:
            return True

    def __credential_checker(self, client, ip):
        """
        Permet de check si l'utilisateur doit crée un compte / a un compte / est ban / kick

        :param client: La connexion socket entre le client et le serveur
        :param ip: l'ip du client
        :return: :bool: si la connexion est réussie
        """
        logged = False
        while not logged and not self.exit_flag.is_set():
            "tant qu'il n'est pas log, attend ses logins"
            __reply = client.recv(1024).decode()
            print(__reply)

            reply = json.loads(__reply)

            print(reply)

            login = reply.get("login", None)
            register = reply.get("register", None)
            close = reply.get("close", None)
            if login:
                user_exist = check_user_exist(user=reply.get("user"), connexion=self.connexion)
                if user_exist:
                    is_ban = check_ban(user=reply.get("user"), ip=ip, connexion=self.connexion)
                    if is_ban:
                        "renvoie false si ban"
                        client.send(str.encode(json.dumps({'login_msg': True, 'login': False, 'ban': True})))
                        return logged

                    is_kick, duree = check_kick(user=reply.get("user"), ip=ip, connexion=self.connexion)
                    print(duree)
                    if is_kick:
                        "renvoie false si kick"
                        client.send(str.encode(json.dumps({'login_msg': True, 'login': False, 'kick': duree})))
                        return logged
                    print(self.user_conn)
                    if reply.get("user") in self.user_conn:
                        client.send(str.encode(json.dumps({'login_msg': True, 'login': False, 'already_logged': True})))
                        return None

                        
                    username, password = get_user_pwd(reply.get("user"), connexion=self.connexion)
                    if username == reply.get("user") and password == reply.get("password"):
                        "check si username / pwd concordent"
                        logged = True
                        self.user_conn[username] = client
                        client.send(str.encode(json.dumps({'login_msg': True, 'login': True})))
                        return logged
                    else:
                        "Username/pwd incorrect"
                        client.send(str.encode(json.dumps({'login_msg': True, 'login': False, 'need_register': False})))

                else:
                    "User existe pas, doit se register"
                    client.send(str.encode(json.dumps({'login_msg': True, 'login': False, 'need_register': True})))
                    
            elif register:
                "Pour le register check si la personne a bien mis aucun espace etc ect (surement le faire depuis le client , a voir)"
                "L'user veut se register, le serveur attend sa nouvelle requete avec l'username et password"


                user_exist = check_user_exist(user=reply.get("user"), connexion=self.connexion)
                print(user_exist)
                if user_exist:
                    "L'utilisateur existe deja, il doit se connecter alors ou se register avec un autre username, le client va lui afficher un message d'erreur, il devra recliquer sur register"
                    client.send(str.encode(json.dumps({'register_msg': True,'register': False})))
                else:
                    is_ban = check_ban(user=reply.get("user"), ip=ip, connexion=self.connexion)
                    if is_ban:
                        "renvoie false si ban"
                        client.send(str.encode(json.dumps({'register_msg': True, 'ban': True,'register': False})))
                        return logged
                    is_kick, duree = check_kick(user=reply.get("user"), ip=ip, connexion=self.connexion)
                    if is_kick:
                        "renvoie false si kick"
                        client.send(str.encode(json.dumps({'register_msg': True, 'login': False, 'kick': duree})))
                        return logged

                    "l'user existe pas, le serveur l'enregiste, renvoie dans la boucle, l'user doit se connecter"
                    print(reply.get("user"), reply.get("password"), ip)
                    register_user(user=reply.get("user"), password=reply.get("password"), ip=ip,
                                  connexion=self.connexion)
                    client.send(str.encode(json.dumps({'register_msg': True,'register': True})))
            elif close:
                "ferme la connexion, le thread ..."
                return logged
        else:
            "si il est log, sort de la boucle et renvoie True pour hdl les messages"
            return logged

    def __accept_clients(self):
        """
        Permet d'accepter les clients jusqu'au nombre max d'users
        """
        rq_thread = Thread(target=self.__channel_rq, args=())
        # rq_thread.start()
        self.threads.append(rq_thread)

        while self.running and not self.exit_flag.is_set():
            while self.m > self.c_user and not self.exit_flag.is_set():
                print("Attente d'un client")
                self.s.listen(self.m)
                client, address = self.s.accept()
                print(f"Nouvelle connexion : {address[0]}")

                thread = Thread(target=self.__client_hdl, args=(client, address[0]))
                self.threads.append(thread)
                self.c_user += 1
                thread.start()

            else:
                print("Max users sur le serveur, attente qu'une place se libère ~30s")
                sleep(30)

    def __message_handler(self, message, client, ip):
        """
        Gere les messages reçu

        :param message: Message reçu du client
        :param client: La connexion entre le client et le serveur
        :return: "stop_connexion" si l'utilisateur a fermer le bot, "relogin" si l'utilisateur s'est déconnecté, sinon None
        """
        print(message)  # debug

        is_kill = message.get("kill", None)
        "Si l'utilisateur veut arreter le serveur"

        is_private = message.get("private_message", None)
        "Si l'utilisateur veut envoyer un message privé a un autre utilisateur"
        is_channel_msg = message.get("channel_message", None)
        "Si l'utilisateur veut envoyer un message dans un channel"

        is_join_channel = message.get("join", None)
        "Si l'utilisateur veut join un channel"
        is_get_joined = message.get("get_joined", None)
        "l'user veut recuperer les channels auquels il a acces"
        
        is_command = message.get("command", None)
        "Si l'utilisateur veut effectuer une commande"

        is_get_status = message.get("get_status", None)
        "Si l'utilisateur veut recuperer les status des users, connectés, déco, idle"
        is_set_status = message.get("set_status", None)
        "Si l'utilisateur veut mettre a jour son status pour les autres users, connectés, déco, idle"

        is_close = message.get("close", None)
        "Si l'utilisateur veut fermer le client"
        is_logout = message.get("logout", None)
        "Si l'utilisateur veut se déconnecter"

        if is_logout:
            "renvoie vers la page de login"
            return "relogin"

        elif is_close:
            if message.get("user", False): self.user_status[message.get("user")] = "deconnected"
            "ferme la connexion, le thread ..."
            return "stop_connexion"

        elif is_get_status:
            "Quand l'utilisateur va get le status toutes les X secondes, il va en meme temps check si il est ban / kick, pour le deconnecter si c'est le cas"
            is_banned = check_ban(user=message.get("user"), ip=ip, connexion=self.connexion)
            is_kicked, duree = check_kick(user=message.get("user"), ip=ip, connexion=self.connexion)
            if is_banned:
                client.send(str.encode(json.dumps({'login_msg': True, 'login': False, 'ban': True})))
                return None
                #le client renvoie stop_connexion

            if is_kicked:
                client.send(str.encode(json.dumps({'login_msg': True, 'login': False, 'kick': duree})))
                return None
                #le client renvoie stop_connexion

            users = get_all_user_name(connexion=self.connexion)
            self.user_status.update({user: "deconnected" for user in users if user not in self.user_status})
            print(self.user_status)
            client.send(str.encode(json.dumps({'get_status': self.user_status})))
            return None

        elif is_set_status:
            self.user_status[message.get("user")] = message.get("set_status")
            return None


        elif is_channel_msg:
            save_channel_message(message=is_channel_msg, channel_name=message.get("channel"),
                                 username=message.get("user"), connexion=self.connexion)
            for conn in self.conn_client:
                if conn != client:
                    conn.send(str.encode(json.dumps(
                        {'channel_message': is_channel_msg, "channel": message.get("channel"),
                         "user": message.get("user")})))
            return None

        elif is_private:
            save_private_message(message=is_private, other_user=message.get("other_user"),
                                 username=message.get("user"), connexion=self.connexion)
            conn = self.user_conn.get(message.get("other_user"))
            conn.send(str.encode(json.dumps(
                {"private_message": is_private, "user": message.get("user")})))
            return None



        elif is_command:
            user = message.get("user")
            if not user == "admin":
                client.send(str.encode(json.dumps({'command': "Not allowed"})))
            else:
                command, user = is_command.split(" ")
                if command == "kick":
                    user, temps = user.split(" ")
                    try:
                        ipaddress.ip_address(user)
                        good, date = kick_user(ip=user, duree=temps, connexion=self.connexion)
                        if good:
                            client.send(str.encode(json.dumps({'command': f"ip kicked until {date} : {user}"})))
                        else:
                            client.send(str.encode(json.dumps({'command': f"ip {user} does not exist"})))
                    except:
                        good, date = kick_user(user=user, duree=temps, connexion=self.connexion)
                        if good:
                            client.send(str.encode(json.dumps({'command': f"user kicked until {date} : {user}"})))
                        else:
                            client.send(str.encode(json.dumps({'command': f"user {user} does not exist"})))


                else:
                    try:
                        ipaddress.ip_address(user)
                        good = ban_user(ip=user, connexion=self.connexion)
                        if good:
                            client.send(str.encode(json.dumps({'command': f"ip banned :{user}"})))
                        else:
                            client.send(str.encode(json.dumps({'command': f"ip {user} does not exist"})))
                    except:
                        good = ban_user(user=user, connexion=self.connexion)
                        if good:
                            client.send(str.encode(json.dumps({'command': f"user banned : {user}"})))
                        else:
                            client.send(str.encode(json.dumps({'command': f"user {user} does not exist"})))
            return None

        elif is_kill:
            user = message.get("user")
            if not user == "admin":
                client.send(str.encode(json.dumps({'kill': "Not allowed"})))

            else:
                for con in self.conn_client:
                    con.send(str.encode(json.dumps({'kill': True})))
                    #les clients doivent ensuite envoyer is_close pour close leur connexion
                sleep(5)
                self.running = False
                self.exit_flag.set()
                sys.exit(0)
            return None


        elif is_join_channel:
            user = message.get("user")
            channel_name = message.get("channel")
            if get_channel_acceptation(channel_name=channel_name, connexion=self.connexion):
                set_new_channel_rq(connexion=self.connexion, username=user, channel_name=channel_name)
            else:
                print('here')
                set_new_channel_rq(connexion=self.connexion, username=user, channel_name=channel_name, status="accept")
                client.send(str.encode(json.dumps({'join': True, "channel_name":channel_name, "status":"accept"})))
            return None

        elif is_get_joined:
            user = message.get("user")
            _ = get_joined_channel_rq(connexion=self.connexion, username=user)
            dict = {"get_joined": True, "dict": _}
            client.send(str.encode(json.dumps(dict)))
            return None




        else:
            "erreur c'est pas normal"

    def __client_hdl(self, new_client, ip):
        closed = False
        while not closed and not self.exit_flag.is_set():
            #new_client.send(str.encode("True"))
            is_logged = self.__credential_checker(client=new_client, ip=ip)
            "Il faut check si l'utilisateur ne ferme pas le client durant la connexion !!"
            if is_logged is None:
                pass
            elif is_logged:
                "Il s'est connecté , on ajoute sa connexion"
                self.conn_client.append(new_client)

                while is_logged and not self.exit_flag.is_set():
                    try:
                        __reply = new_client.recv(1024).decode()
                        print(__reply)
                        reply = json.loads(__reply)

                        status = self.__message_handler(message=reply, client=new_client, ip=ip)
                        if status == "stop_connexion":
                            is_logged = False
                            closed = True
                        if status == "relogin":
                            is_logged = False
                    except ConnectionResetError:
                        is_logged = False
                        closed = True

                else:
                    "il a cliquer sur le bouton deconnecté, on va attendre qu'il se register / se reconnecter"
                    self.conn_client.remove(new_client)
                    self.user_conn = {key: val for key, val in self.user_conn.items() if val != new_client}
            else:
                "L'user est ban / kick, on ferme la connexion"
                closed = True

        else:
            "l'user a fermer son client, on supprime donc sa connexion, son thread et on enleve un user"
            new_client.close()
            try:
                self.user_conn = {key: val for key, val in self.user_conn.items() if val != new_client}
                self.conn_client.remove(new_client)
                self.c_user -= 1
                self.threads.remove(current_thread())
            except ValueError:
                pass

    def start(self):
        """
        Start la classe
        """
        bind = self.__bind()
        if not bind:
            self.running = False
        self.connexion = check_bdd(host=self.ip_bdd)
        if not self.connexion:
            self.running = False

        while self.running and not self.exit_flag.is_set():
            self.__accept_clients()
        else:
            print("ERROR")


if __name__ == "__main__":
    Server(ip="192.168.1.19", port=6530, max_user=3, ip_bdd="192.168.1.19").start()

