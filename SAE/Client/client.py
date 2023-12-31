import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPlainTextEdit, QSpacerItem, QMessageBox, QSizePolicy, QLabel, QLineEdit, QPushButton, QMainWindow, QFrame, QVBoxLayout, QStackedWidget, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt5 import QtGui, QtCore
from threading import Thread, Event
import socket
import json
from time import sleep
from PyQt5.QtCore import QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
import os

class MainWindow(QMainWindow):
    signal = pyqtSignal(str)
    def __init__(self, ip:str, port:int):
        super().__init__()

        #Variables de classes permettant le bon fonctionnement du client
        self.is_running = True
        self.__exit_flag = Event()
        self.__is_mp_btn_clicked = False
        self.__is_login_page = True
        self.__logged = False
        self.__refresh = False
        self.__ip = ip
        self.__port = port
        self.__thread = []
        self.__user_status = {}
        self.__username = ""
        self.__cache = {"Général": [], "Blabla": [], "Comptabilité": [], "Informatique": [], "Marketing": []}
        #ajoute au buffer des qu'un msg est recu (pour les channels, check si l'user a bien acces aux channels)
        self.__last_item_clicked = None
        self.__channels_join = {} # nom du channel : status ( accepted / pending / refused )
        self.__channels = {"Général": "accept", "Blabla": None, "Comptabilité": None, "Informatique": None, "Marketing": None}


        self.resize(800, 700)
        self.setWindowTitle("Chat APP | Login page")

        self.__centralwidget = QWidget(self)
        self.__stackedWidget = QStackedWidget(self.__centralwidget)

        self.__page = QWidget()
        self.__login_page = QVBoxLayout(self.__page)
        self.__frame = QFrame(self.__page)
        self.__login_layout = QGridLayout(self.__frame)


        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.__username_label_login = QLabel(self.__frame)
        self.__username_label_login.setFont(font)
        self.__username_label_login.setText("USERNAME")
        self.__username_label_login.setMinimumSize(QtCore.QSize(150, 0))
        self.__username_label_login.setMaximumSize(QtCore.QSize(100, 16777215))


        font = QtGui.QFont()
        font.setPointSize(12)
        self.__username_line_edit_login = QLineEdit(self.__frame)
        self.__username_line_edit_login.setMinimumSize(QtCore.QSize(0, 35))
        self.__username_line_edit_login.setMaximumSize(QtCore.QSize(300, 16777215))
        self.__username_line_edit_login.setFont(font)
        self.__username_line_edit_login.setText("")
        regex = QRegExp("^[a-zA-Z0-9]+$")
        validator = QRegExpValidator(regex, self.__username_line_edit_login)
        self.__username_line_edit_login.setValidator(validator)


        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.__password_label_login = QLabel(self.__frame)
        self.__password_label_login.setFont(font)
        self.__password_label_login.setText("MOT DE PASSE")
        self.__password_label_login.setMinimumSize(QtCore.QSize(150, 0))
        self.__password_label_login.setMaximumSize(QtCore.QSize(100, 16777215))


        font = QtGui.QFont()
        font.setPointSize(12)
        self.__password_line_edit_login = QLineEdit(self.__frame)
        self.__password_line_edit_login.setMinimumSize(QtCore.QSize(0, 35))
        self.__password_line_edit_login.setMaximumSize(QtCore.QSize(300, 16777215))
        self.__password_line_edit_login.setFont(font)
        self.__password_line_edit_login.setText("")
        regex = QRegExp("^[A-Za-z\d@$!%*?&]*$")
        validator = QRegExpValidator(regex, self.__password_line_edit_login)
        self.__password_line_edit_login.setValidator(validator)


        self.__login_layout.addWidget(self.__username_line_edit_login, 0, 1, 1, 1)
        self.__login_layout.addWidget(self.__username_label_login, 0, 0, 1, 1)
        self.__login_layout.addWidget(self.__password_line_edit_login, 1, 1, 1, 1)
        self.__login_layout.addWidget(self.__password_label_login, 1, 0, 1, 1)

        self.__login_page.addWidget(self.__frame)

        self.widget = QWidget(self.__page)
        self.__btn_login_layout = QVBoxLayout(self.widget)

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.__btn_submit_login = QPushButton(self.widget)
        self.__btn_submit_login.setMinimumSize(QtCore.QSize(300, 50))
        self.__btn_submit_login.setMaximumSize(QtCore.QSize(0, 0))
        self.__btn_submit_login.setFont(font)
        self.__btn_submit_login.setText("SUBMIT LOGIN")

        spacerItem = QSpacerItem(0, 80, QSizePolicy.Minimum, QSizePolicy.Fixed)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.__btn_switch_to_register = QPushButton(self.widget)
        self.__btn_switch_to_register.setMinimumSize(QtCore.QSize(200, 35))
        self.__btn_switch_to_register.setMaximumSize(QtCore.QSize(0, 0))


        self.__btn_switch_to_register.setFont(font)
        self.__btn_switch_to_register.setText("REGISTER PAGE")

        self.__btn_login_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.__btn_login_layout.addWidget(self.__btn_submit_login, 0, QtCore.Qt.AlignCenter)
        self.__btn_login_layout.addItem(spacerItem)
        self.__btn_login_layout.addWidget(self.__btn_switch_to_register, 0, QtCore.Qt.AlignCenter)

        self.__login_page.addWidget(self.widget)

        self.__stackedWidget.addWidget(self.__page)

        self.__page_2 = QWidget()
        self.__message_page = QGridLayout(self.__page_2)

        self.widget_2 = QWidget(self.__page_2)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_2.setMaximumSize(QtCore.QSize(10000, 50))
        self.nav = QHBoxLayout(self.widget_2)


        font = QtGui.QFont()
        font.setPointSize(10)
        self.__private_msg_btn = QPushButton(self.widget_2)
        self.__private_msg_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.__private_msg_btn.setFont(font)
        self.__private_msg_btn.setText("Messages Privés")


        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(50)
        self.__channel_msg_btn = QPushButton(self.widget_2)
        self.__channel_msg_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.__channel_msg_btn.setFont(font)
        self.__channel_msg_btn.setText("Messages Publiques")

        self.nav.addWidget(self.__private_msg_btn)
        self.nav.addWidget(self.__channel_msg_btn)

        self.widget_3 = QWidget(self.__page_2)
        self.__message_box = QGridLayout(self.widget_3)

        self.__list_message_box = QListWidget(self.widget_3)

        self.__show_message_box = QPlainTextEdit(self.widget_3)
        self.__show_message_box.setMaximumSize(QtCore.QSize(16777215, 10000))
        self.__show_message_box.setReadOnly(True)


        font = QtGui.QFont()
        font.setPointSize(12)
        self.__send_message_box = QLineEdit(self.widget_3)
        self.__send_message_box.setMinimumSize(QtCore.QSize(0, 35))
        self.__send_message_box.setFont(font)
        self.__send_message_box.setText("")

        self.__message_box.addWidget(self.__list_message_box, 0, 0, 2, 1)
        self.__message_box.addWidget(self.__show_message_box, 0, 1, 1, 1)
        self.__message_box.addWidget(self.__send_message_box, 1, 1, 1, 1)

        self.__message_page.addWidget(self.widget_2, 0, 0, 1, 1)
        self.__message_page.addWidget(self.widget_3, 1, 0, 1, 1)

        self.__stackedWidget.addWidget(self.__page_2)

        self.setCentralWidget(self.__stackedWidget)

        self.__setup_public_msg()

        self.__stackedWidget.setCurrentIndex(0)

        self.show()

        self.__bind_socket()

        self.__private_msg_btn.clicked.connect(self.__btn_private_clicked)
        self.__channel_msg_btn.clicked.connect(self.__btn_channel_clicked)
        self.__list_message_box.itemClicked.connect(self.__handle_btn_msg)
        self.__btn_submit_login.clicked.connect(self.__handle_login)
        self.__btn_switch_to_register.clicked.connect(self.__switch_register_login)
        self.__send_message_box.returnPressed.connect(self.__handle_send_msg)
        self.signal.connect(self.__handle_signal)

    def __handle_signal(self, result):
        kill, title, msg = result.split(":")
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        button_clicked = msg_box.exec_()
        if kill == "kill" and button_clicked == QMessageBox.Ok:
            self.__close_app()

    def closeEvent(self, event):
        """
        Cette fonction est permet d'ajouter des étapes quand l'utilisateur clique pour fermer l'app
        Ici il ferme le socket et envoie un message au serveur
        :param event: Close event
        """
        self.__close_app()
        event.accept()

    def __handle_reply(self, reply):
        """
        Cette fonction est utilisé pour gérer les messages que le client reçois du serveur
        :param reply: dict format json
        :return: is_logged, is_banned, kick_time, need_register, already_logged (Tous le temps False sauf si l'utilisateur fait appel a cette fonction pour se connecter)
        """
        is_login = reply.get("login_msg", None) # Réponse par rapport a l'authentification
        is_register = reply.get("register_msg", None) # Réponse par rapport a l'enregistrement d'un nouvel user
        is_channel_message = reply.get("channel_message", None) # Nouveau message reçu dans un channel
        is_private_message = reply.get("private_message", None) # Nouveau message privé reçu
        is_command = reply.get("command", None) # Réponse par rapport a une commande effectuée
        is_kill = reply.get("kill", None) # Réponse par rapport au Kill
        is_get_status = reply.get("get_status", None) # Réponse pour recuperer tous les status des users enregistrer sur la bdd
        is_get_joined = reply.get("get_joined", None) # Réponse pour recuperer tous les channels où l'utilisateur à access, si la demande est déja faite ou si il s'est fait refusé
        is_join = reply.get("join", None) # Réponse à la demande pour rejoindre un channel

        # print(reply) #debug

        if is_register:
            return reply.get("register"), reply.get("ban", False), reply.get("kick", False) #True / False si bien registered ou pas, idem pour ban, datetime / False si il est kick

        elif is_login:
            is_logged = reply.get("login", False) # Sait si l'authentification de l'utilisateur s'est bien déroulé
            is_banned = reply.get("ban", False) # si l'utilisateur est ban / son ip
            kick_time = reply.get("kick", False) # si l'utilisateur est kick / son ip
            need_register = reply.get("need_register", False) # si l'utilisateur (son username) n'existe pas, il doit crée un compte
            already_logged = reply.get("already_logged", False) # si l'utilisateur est déja connecté sur une autre machine

            return is_logged, is_banned, kick_time, need_register, already_logged

        elif is_channel_message: # Message d'un autre user recu, a mettre dans un channel, l'ajoute au cache et l'affiche si l'utilisateur est dessus
            message = is_channel_message
            sender = reply.get("user", None)
            channel_name = reply.get("channel", None)
            self.__cache[channel_name].append(f"{sender}> {message}")
            # print(f"last item {self.__last_item_clicked}, channel_name {channel_name}")
            if self.__last_item_clicked == channel_name:
                # print("append")
                self.__show_message_box.appendPlainText(f"{sender}> {message}")


        elif is_private_message: # Message privé d'un autre user recu , l'ajoute au cache et l'affiche si l'utilisateur est dessus
            message = is_private_message
            sender = reply.get("user", None)
            if not self.__cache.get("sender", False):
                self.__cache[sender] = []
            self.__cache[sender].append(f"{sender}> {message}")

            if self.__last_item_clicked == sender:
                self.__show_message_box.appendPlainText(f"{sender}> {message}")

        elif is_command: # Verifie si la commande est passée
            if is_command == "Not allowed":
                self.signal.emit("None:Erreur Commande:Tu n'as pas le droit d'effectuer une commande")
            else:
                self.signal.emit(f"None:Info Commande:Votre commande a été effectué \n réponse du serveur : {is_command}")


        elif is_kill: # Verifie si le kill est bien passé
            if is_kill == "Not allowed":
                self.signal.emit(f"None:Erreur Kill:Tu n'as pas le droit de kill le serveur")

            else:
                self.is_running = False
                self.__exit_flag.set()
                self.signal.emit("kill:Stop:Le serveur doit s'arreter")

        elif is_get_status: # Récupere le status de tous les users, supprime le sien du dictionnaire, et gère l'affichage si il y'a un nouvel user, si le client est sur la bonne page ...
            del is_get_status[self.__username]
            # print(self.__last_item_clicked)
            if self.__refresh and self.__is_mp_btn_clicked:
                self.__setup_private_msg()
                self.__user_status = is_get_status
                self.__refresh = False

            elif not self.__is_mp_btn_clicked and is_get_status != self.__user_status:
                self.__user_status = is_get_status
                self.__refresh = True

            elif self.__is_mp_btn_clicked and is_get_status != self.__user_status:
                self.__user_status = is_get_status
                self.__setup_private_msg()

            for user in self.__user_status:
                if not self.__cache.get(user, None):
                    self.__cache[user] = []


            # del is_get_status[self.__username]
            # self.__user_status = is_get_status
            # if self.__user_status.get(self.__last_item_clicked, False) or self.__is_mp_btn_clicked:
            #     #l'user est dans la section private msg donc il faut update les boutons
            #     self.__setup_private_msg()


        elif is_get_joined: # Message reçu lors du login, pour ne pas envoyer plusieurs fois des requetes pour rejoindre un channel si la requete est deja faite
            dict = reply.get("dict")
            for channel, status in dict.items():
                self.__channels[channel] = status

        elif is_join: # Récupere le status de la demande pour rejoindre un channel, accepté ou refusé
            channel_name = reply.get("channel_name")
            status = "accepté" if reply.get("status") == "accept" else "refusé"
            self.__channels[channel_name] = reply.get("status")
            self.signal.emit(f"None:Demande Channel {channel_name}:Votre demande pour le channel {channel_name} a été {status}")

            # QMessageBox.information(self, f"Demande Channel {channel_name}",f"Votre demande pour le channel {channel_name} a été {status}")

        return False, False, False, False, False


    def __handle_send_msg(self):
        """
        Cette fonction est appelée quand la touche entrée est cliqué, cad pour envoyer un message.
        Elle regarde si c'est un message privé ou alors dans un channel, l'ajoute au cache et envoie un message au serveur
        """
        try:
            msg = self.__send_message_box.text()
            self.__send_message_box.clear()
            # print("handle1",self.__last_item_clicked, self.__is_mp_btn_clicked, self.__cache)
            if self.__last_item_clicked: # si il est différent de None, cela veut dire que le client a cliqué sur soit un autre user soit un channel
                if self.__is_mp_btn_clicked: # gère si c'est un mp
                    self.__cache[self.__last_item_clicked].append(f"moi> {msg}")
                    self.__show_message_box.appendPlainText(f"moi> {msg}")
                    # print("handle2",self.__cache, self.__user_status.get(self.__last_item_clicked))
                    if self.__user_status.get(self.__last_item_clicked) != "deconnected":
                        self.s.send(str.encode(
                            json.dumps({'private_message': msg, "user": self.__username, "other_user": self.__last_item_clicked})))

                else: # gère si c'est un message dans un channel
                    self.s.send(str.encode(json.dumps({'channel_message': msg, "user": self.__username, "channel": self.__last_item_clicked})))
                    self.__cache[self.__last_item_clicked].append(f"moi> {msg}")
                    self.__show_message_box.appendPlainText(f"moi> {msg}")
        except Exception as e:
            print(e)


    def __handle_login(self):
        """
        Gestion du login / register en plusieurs étapes (verification de l'input, envoi du message vers le server)

        Cette fonction permet de vérifier:
            - L'username min 3 caracteres / max 20 / pas d'espaces / pas de caractères spéciaux
            - Le password min 3 caracteres / max 20 / pas d'espaces / certains caractères spéciaux

        Permet aussi de gerer les réponses du serveurs pour savoir si on est correctement connecté / si on s'est correctement crée un compte
        """
        # check si username n'a pas de caractere spéciaux, espace etc etc, pareil pour le mdp

        username = self.__username_line_edit_login.text()

        if not username:
            return QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom d'utilisateur.")
        elif len(username) < 3:
            return QMessageBox.warning(self, "Erreur", "Le nom d'utilisateur doit contenir au moins 3 caractères.")
        elif len(username) > 20:
            return QMessageBox.warning(self, "Erreur", "Le nom d'utilisateur doit contenir moins de 20 caractères.")

        password = self.__password_line_edit_login.text()

        if not password:
            return QMessageBox.warning(self, "Erreur", "Veuillez entrer un password.")
        elif len(password) < 3:
            return QMessageBox.warning(self, "Erreur", "Le password doit contenir au moins 3 caractères.")
        elif len(password) > 20:
            return QMessageBox.warning(self, "Erreur", "Le password doit contenir moins de 20 caractères.")

        if self.__is_login_page: #L'utilisateur veut se log
            "il n'a pas switch sur la page de register, il veut donc se log"
           # __reply = self.s.recv(1024).decode() je crois pas besoin de cette ligne, je crois que ca sert a rien d'envoyer un msg etc etc
            __reply = True
            if __reply:

                self.s.send(str.encode(json.dumps({'login': True, "user": username, "password": password})))
                __reply = self.s.recv(1024).decode()
                reply = json.loads(__reply)

                is_logged, is_banned, kick_time, need_register, already_logged = self.__handle_reply(reply)

                if is_logged: # Si l'authentification est un succes
                    t = Thread(target=self.__receive_msg, args=(), name="receive_socket_msg").start()
                    self.__thread.append(t)
                    t = Thread(target=self.__get_status, args=(), name="get_status").start()
                    self.__thread.append(t)
                    self.s.send(str.encode(json.dumps({'get_joined': True, "user": username})))
                    self.__stackedWidget.setCurrentIndex(1)
                    self.setWindowTitle(f"Chat APP | Connecté en tant que : {username}")
                    self.__logged = True
                    self.__username = username
                    self.__set_status()
                elif already_logged: # Si il est connecté sur une autre machine
                    return QMessageBox.warning(self, "Erreur", "Ton compte est déjà connecté sur une autre machine !")
                elif is_banned: # si l'ip ou l'username est banni
                    QMessageBox.warning(self, "Erreur", "Ton ip ou ton username est banni !")
                    self.__close_app()
                    return
                elif kick_time: # si l'ip ou l'username est kick
                    QMessageBox.warning(self, "Erreur", f"Ton ip ou ton username est kick jusqu'au {kick_time}!")
                    self.__close_app()
                    return
                elif not is_logged and need_register: # si l'user existe pas, doit se register dans ce cas
                    return QMessageBox.warning(self, "User Inexistant",f"Tu as besoin de te register, aucun compte existe au nom d'{username}")
                elif not is_logged and not need_register: # Si mauvais mdp
                    return QMessageBox.warning(self, "User / mdp incorrect",f"Cette combinaison d'username / mdp n'est pas la bonne, réessaye !")
                else:
                    # return print("Aucune idée du soucis")
                    return

            else:
                "erreur avec le serv"
        else:
            "il veut se register"
            #__reply = self.s.recv(1024).decode()
            __reply = True
            if __reply: #il veut s'enregister
                self.s.send(str.encode(json.dumps({'register': True, "user": username, "password": password})))
                __reply = self.s.recv(1024).decode()
                reply = json.loads(__reply)
                is_registered, is_ban, kick_time = self.__handle_reply(reply)
                # print(is_registered, is_ban, kick_time)
                if is_registered and not is_ban and not kick_time: # L'enregistrement est un succes
                    return QMessageBox.information(self, "Register", "Vous avez bien été enregistré")
                elif not is_registered and not is_ban and not kick_time: # Cet username existe deja
                    return QMessageBox.warning(self, "User Existant",f"L'username : {username} existe déjà")
                elif not is_registered and not is_ban and kick_time: # son ip ou cet username est kick
                    QMessageBox.warning(self, "Erreur", f"Ton ip ou ton username est kick jusqu'au {kick_time}!")
                    self.__close_app()
                    return
                else: # Son ip ou son username est banni
                    QMessageBox.warning(self, "Erreur", "Ton ip ou ton username est banni !")
                    self.__close_app()
                    return



    def __switch_register_login(self):
        """
        Cette fonction est utilisé lorsque la personne clique sur le bouton pour
        se register par exemple, cela renomme donc les labels et les boutons
        """
        if self.__is_login_page: #PAge de login, afficher les informations adéquates
            self.__btn_switch_to_register.setText("LOGIN PAGE")
            self.__btn_submit_login.setText("SUBMIT REGISTER")
            self.__username_label_login.setText("NEW USERNAME")
            self.__password_label_login.setText("NEW PASSWORD")
            self.__is_login_page = False
            self.setWindowTitle("Register page")
        else: # Page de register , idem afficher les bonnes informations
            self.__btn_switch_to_register.setText("REGISTER PAGE")
            self.__btn_submit_login.setText("SUBMIT LOGIN")
            self.__username_label_login.setText("USERNAME")
            self.__password_label_login.setText("PASSWORD")
            self.__is_login_page = True
            self.setWindowTitle("Login page")



    def __handle_btn_msg(self, item):
        """
        Cette fonction est utilisée lorsque le client appuye sur un item de la QListWidget,
        verifie si c'est un user ou si c'est un channel pour que l'utilisateur puisse demander
        un acces, mettre un message d'erreur si son acces a ce channel est refusé par le serveur
        ou si il a deja fait sa demande et met en mémoire le dernier item cliqué (le nom
        du channel ou de l'utilisateur)

        :param item: L'item cliqué
        """

        if self.__last_item_clicked != item.text().split("[")[0] and not self.__is_mp_btn_clicked: #Il a cliqué sur un autre channel que le précedent, il faut check si il a acces
            if not self.__channels.get(item.text().split("[")[0], False): #Il n'a pas acces, il doit faire sa demande
                self.__last_item_clicked = None
                message_box = QMessageBox()
                message_box.setWindowTitle("Demande")
                message_box.setText(f"Voulez-vous faire la demande pour rejoindre le channel : {item.text().split('[')[0]}")
                dmd_btn = message_box.addButton("Faire la demande", QMessageBox.AcceptRole)
                cancel_btn = message_box.addButton("Annuler", QMessageBox.RejectRole)
                message_box.exec_()
                if message_box.clickedButton() == dmd_btn: # Si il veut faire sa demande
                    self.__channels[item.text().split("[")[0]] = "pending"
                    # print(self.__channels)
                    self.s.send(str.encode(json.dumps({'join': True, "user": self.__username, "channel": item.text().split("[")[0]})))
                    return
                elif message_box.clickedButton() == cancel_btn: # Si il ne veut pas faire sa demande
                    return

            elif self.__channels.get(item.text().split("[")[0], False) == "pending": # Une demande est déja en cours
                self.__last_item_clicked = None
                return QMessageBox.information(self, f"Demande channel {item.text().split('[')[0]}", f"Votre demande pour le channel {item.text().split('[')[0]} est en attente, il faut que le serveur accepte votre demande !")

            elif self.__channels.get(item.text().split("[")[0], False) == "refuse": # Sa demande s'est faite refusé, il n'aura jamais acces
                self.__last_item_clicked = None
                return QMessageBox.Warning(self, f"Demande channel {item.text().split('[')[0]}", f"Votre demande pour le channel {item.text().split('[')[0]} à été refusé, vous ne pourrez pas avoir accès à ce channel")

            else: # Il a access, il faut donc afficher les anciens messages depuis le cache
                self.__show_message_box.setPlainText("\n".join(self.__cache[item.text().split("[")[0]]))
                self.__last_item_clicked = item.text().split("[")[0].replace(" ", "")
                # print("else", item.text().split("[")[0], self.__last_item_clicked)

        elif self.__last_item_clicked != item.text().split("[")[0].replace(" ", "") and self.__is_mp_btn_clicked: # C'est un message privé, il a forcement acces, il faut donc afficher les messages depuis le cache
            self.__last_item_clicked = item.text().split("[")[0].replace(" ", "")
            self.__show_message_box.clear()
            # print('new box clicked', self.__cache.get(self.__last_item_clicked), self.__cache)
            if self.__cache.get(self.__last_item_clicked):
                self.__show_message_box.setPlainText("\n".join(self.__cache[self.__last_item_clicked])) # Pas sur a test
    def __btn_channel_clicked(self):
        """
        Cette fonction est utilisé pour afficher la page des channels ( et de ne pas la réaffiché si elle est déja affiché )
        """
        if not self.__is_mp_btn_clicked:
            return
        self.__setup_public_msg()
        self.__is_mp_btn_clicked = False

    def __btn_private_clicked(self):
        """
        Cette fonction est utilisé pour afficher la page des messages privés ( et de ne pas la réaffiché si elle est déja affiché )
        :return:
        """
        if self.__is_mp_btn_clicked:
            return
        self.__setup_private_msg()
        self.__is_mp_btn_clicked = True



    def __bind_socket(self):
        """
        Cette fonction est utilisé pour se connecter au serveur, et gérer les erreurs de connexions
        """
        self.s = socket.socket()
        try:
            self.s.connect((self.__ip, self.__port))
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error connecting with the server, closing App when you click on button")
            msg.setInformativeText(f'{e}')
            msg.setWindowTitle("Error")
            msg.exec_()
            self.__close_app()



    def __setup_public_msg(self):
        """
        Cette fonction permet de générer l'affichage des channels dans la QListWidget
        """
        self.__list_message_box.clear()
        self.__show_message_box.clear()


        for channel in self.__channels: # Permet d'ajouter les boutons dans le QListWidget (les boutons pour voir les messages des channels)
            item = QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(channel)
            self.__list_message_box.addItem(item)

    def __setup_private_msg(self):
        """
        Cette fonction permet de générer l'affichage des utilisateurs dans la QListWidget (pour les messages privés)
        """
        self.__list_message_box.clear()
        self.__show_message_box.clear()

        for user, status in self.__user_status.items(): # Permet d'ajouter les boutons dans le QListWidget (les boutons pour voir les mp)
            item = QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(f"{user} [{status.upper()}]")
            self.__list_message_box.addItem(item)


    def __receive_msg(self):
        """
        Cette fonction, utilisée dans un thread, permet de récupérer continuellement les messages reçu depuis le serveur
        et les envois dans la fonction handle_reply
        """
        while self.is_running and not self.__exit_flag.is_set():
            try:
                __reply = self.s.recv(1024).decode()
                reply = json.loads(__reply) #permet de charger un str() en dict() json
                # print(reply)
                is_logged, is_banned, kick_time, need_register, already_logged = self.__handle_reply(reply) #Permet de check si l'utilisateur est ban ou kick, et envoie les messages recu dans cette fonction pour qu'elle les gere
                if is_banned:
                    self.signal.emit("kill:Erreur:Ton ip ou ton username est banni !")
                    # QMessageBox.warning(self, "Erreur", "Ton ip ou ton username est banni !")
                    # self.__close_app()
                    return
                elif kick_time:
                    self.signal.emit(f"kill:Erreur:on ip ou ton username est kick jusqu'au {kick_time}!")
                    # QMessageBox.warning(self, "Erreur", f"Ton ip ou ton username est kick jusqu'au {kick_time}!")
                    # self.__close_app()
                    return
                else:
                    pass
            except (ConnectionAbortedError, TypeError):
                pass




    def __close_app(self):
        """
        Permet de fermer proprement l'application en fermant le socket, et en prévenant le serveur de l'arret du client
        """
        self.is_running = False
        self.__exit_flag.set()

        try:
            # if self.__logged:
            #     self.__set_status(status="deconnected")
            if self.__username: self.s.send(str.encode(json.dumps({'close': True, "user": self.__username}))) #Si l'utilisateur est déja log, il faut dire au serveur de mettre son status en deconnected
            else: self.s.send(str.encode(json.dumps({'close': True}))) #Dis au serveur que le client se ferme
            self.s.close()
        except:
            pass
        QApplication.closeAllWindows() #Ferme les fenetres
        os._exit(os.EX_OK) #Quitte l'application

    def __set_status(self, status="connected"):
        """
        Cette fonction permet d'envoyer une requete vers le serveur pour définir le status du client
        :param status: connected par défault, sinon le status a envoyer au serveur
        """
        self.s.send(str.encode(json.dumps({'set_status': status, "user": self.__username})))

    def __get_status(self):
        """
        Cette fonction utilisée dans un thread permet de d'envoyer toutes les 5 secondes une demande pour recuperer
        le status de tous les users, donc si il y'a un nouvel utilisateur, si un user se deconnecte ... Le client
        récupera l'information grace a cette requete
        """
        while self.is_running and not self.__exit_flag.is_set():
            try:
                self.s.send(str.encode(json.dumps({'get_status': True, "user": self.__username})))
                sleep(5)
            except ConnectionResetError:
                sleep(5) #le serveur s'est arreter mais le client veut envoyer un message, il n'a pas encore actualisé le fait que self.is_running = False


def start_client(ip,port):
    """
    Cette fonction permet de start le client, en créant une instance de QApplication ainsi que de la MainWindow
    :param ip: L'ip du serveur que le client doit contacter
    :param port: Le port du serveur que le client doit contacter
    """
    app = QApplication(sys.argv)
    window = MainWindow(ip=ip,port=port)
    #window.show()
    app.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(ip="192.168.1.19",port=6530)
    #window.show()
    app.exec()
