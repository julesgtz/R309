
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPlainTextEdit, QSpacerItem, QMessageBox, QSizePolicy, QLabel, QLineEdit, QPushButton, QMainWindow, QFrame, QVBoxLayout, QStackedWidget, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt5 import QtGui, QtCore
from threading import Thread
import socket
import json
from time import sleep
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

class MainWindow(QMainWindow):
    def __init__(self, ip:str, port:int):
        super().__init__()

        self.is_running = True
        self.is_mp_btn_clicked = False
        self.is_login_page = True
        self.logged = False
        self.refresh = False
        self.ip = ip
        self.port = port
        self.thread = []
        self.user_status = {}
        self.username = ""
        self.cache = {"Général": [], "Blabla": [], "Comptabilité": [], "Informatique": [], "Marketing": []}
        #ajoute au buffer des qu'un msg est recu (pour les channels, check si l'user a bien acces aux channels)
        self.last_item_clicked = None
        self.channels_join = {} # nom du channel : status ( accepted / pending / refused )
        self.channels = {"Général": "accept", "Blabla": None, "Comptabilité": None, "Informatique": None, "Marketing": None}
        self.new_status = {}


        self.resize(800, 700)
        self.setWindowTitle("Chat APP | Login page")

        self.centralwidget = QWidget(self)
        self.stackedWidget = QStackedWidget(self.centralwidget)

        self.page = QWidget()
        self.login_page = QVBoxLayout(self.page)
        self.frame = QFrame(self.page)
        self.login_layout = QGridLayout(self.frame)


        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.username_label_login = QLabel(self.frame)
        self.username_label_login.setFont(font)
        self.username_label_login.setText("USERNAME")
        self.username_label_login.setMinimumSize(QtCore.QSize(150, 0))
        self.username_label_login.setMaximumSize(QtCore.QSize(100, 16777215))


        font = QtGui.QFont()
        font.setPointSize(12)
        self.username_line_edit_login = QLineEdit(self.frame)
        self.username_line_edit_login.setMinimumSize(QtCore.QSize(0, 35))
        self.username_line_edit_login.setMaximumSize(QtCore.QSize(300, 16777215))
        self.username_line_edit_login.setFont(font)
        self.username_line_edit_login.setText("")
        regex = QRegExp("^[a-zA-Z0-9]+$")
        validator = QRegExpValidator(regex, self.username_line_edit_login)
        self.username_line_edit_login.setValidator(validator)


        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.password_label_login = QLabel(self.frame)
        self.password_label_login.setFont(font)
        self.password_label_login.setText("MOT DE PASSE")
        self.password_label_login.setMinimumSize(QtCore.QSize(150, 0))
        self.password_label_login.setMaximumSize(QtCore.QSize(100, 16777215))


        font = QtGui.QFont()
        font.setPointSize(12)
        self.password_line_edit_login = QLineEdit(self.frame)
        self.password_line_edit_login.setMinimumSize(QtCore.QSize(0, 35))
        self.password_line_edit_login.setMaximumSize(QtCore.QSize(300, 16777215))
        self.password_line_edit_login.setFont(font)
        self.password_line_edit_login.setText("")
        regex = QRegExp("^[A-Za-z\d@$!%*?&]*$")
        validator = QRegExpValidator(regex, self.password_line_edit_login)
        self.password_line_edit_login.setValidator(validator)


        self.login_layout.addWidget(self.username_line_edit_login, 0, 1, 1, 1)
        self.login_layout.addWidget(self.username_label_login, 0, 0, 1, 1)
        self.login_layout.addWidget(self.password_line_edit_login, 1, 1, 1, 1)
        self.login_layout.addWidget(self.password_label_login, 1, 0, 1, 1)

        self.login_page.addWidget(self.frame)

        self.widget = QWidget(self.page)
        self.btn_login_layout = QVBoxLayout(self.widget)

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_submit_login = QPushButton(self.widget)
        self.btn_submit_login.setMinimumSize(QtCore.QSize(300, 50))
        self.btn_submit_login.setMaximumSize(QtCore.QSize(0, 0))
        self.btn_submit_login.setFont(font)
        self.btn_submit_login.setText("SUBMIT LOGIN")

        spacerItem = QSpacerItem(0, 80, QSizePolicy.Minimum, QSizePolicy.Fixed)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.btn_switch_to_register = QPushButton(self.widget)
        self.btn_switch_to_register.setMinimumSize(QtCore.QSize(200, 35))
        self.btn_switch_to_register.setMaximumSize(QtCore.QSize(0, 0))


        self.btn_switch_to_register.setFont(font)
        self.btn_switch_to_register.setText("REGISTER PAGE")

        self.btn_login_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.btn_login_layout.addWidget(self.btn_submit_login, 0, QtCore.Qt.AlignCenter)
        self.btn_login_layout.addItem(spacerItem)
        self.btn_login_layout.addWidget(self.btn_switch_to_register, 0, QtCore.Qt.AlignCenter)

        self.login_page.addWidget(self.widget)

        self.stackedWidget.addWidget(self.page)

        self.page_2 = QWidget()
        self.message_page = QGridLayout(self.page_2)

        self.widget_2 = QWidget(self.page_2)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_2.setMaximumSize(QtCore.QSize(10000, 50))
        self.nav = QHBoxLayout(self.widget_2)


        font = QtGui.QFont()
        font.setPointSize(10)
        self.private_msg_btn = QPushButton(self.widget_2)
        self.private_msg_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.private_msg_btn.setFont(font)
        self.private_msg_btn.setText("Messages Privés")


        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(50)
        self.channel_msg_btn = QPushButton(self.widget_2)
        self.channel_msg_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.channel_msg_btn.setFont(font)
        self.channel_msg_btn.setText("Messages Publiques")

        self.nav.addWidget(self.private_msg_btn)
        self.nav.addWidget(self.channel_msg_btn)

        self.widget_3 = QWidget(self.page_2)
        self.message_box = QGridLayout(self.widget_3)

        self.list_message_box = QListWidget(self.widget_3)

        self.show_message_box = QPlainTextEdit(self.widget_3)
        self.show_message_box.setMaximumSize(QtCore.QSize(16777215, 10000))
        self.show_message_box.setReadOnly(True)


        font = QtGui.QFont()
        font.setPointSize(12)
        self.send_message_box = QLineEdit(self.widget_3)
        self.send_message_box.setMinimumSize(QtCore.QSize(0, 35))
        self.send_message_box.setFont(font)
        self.send_message_box.setText("")

        self.message_box.addWidget(self.list_message_box, 0, 0, 2, 1)
        self.message_box.addWidget(self.show_message_box, 0, 1, 1, 1)
        self.message_box.addWidget(self.send_message_box, 1, 1, 1, 1)

        self.message_page.addWidget(self.widget_2, 0, 0, 1, 1)
        self.message_page.addWidget(self.widget_3, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.setCentralWidget(self.stackedWidget)

        self.setup_public_msg()

        self.stackedWidget.setCurrentIndex(0)

        self.show()

        self.bind_socket()

        self.private_msg_btn.clicked.connect(self.btn_private_clicked)
        self.channel_msg_btn.clicked.connect(self.btn_channel_clicked)
        self.list_message_box.itemClicked.connect(self.handle_btn_msg)
        self.btn_submit_login.clicked.connect(self.handle_login)
        self.btn_switch_to_register.clicked.connect(self.switch_register_login)
        self.send_message_box.returnPressed.connect(self.handle_send_msg)


    def closeEvent(self, event):
        print("closing")
        self.close_app()
        event.accept()

    def handle_reply(self, reply):
        is_login = reply.get("login_msg", None)
        is_register = reply.get("register_msg", None)
        is_channel_message = reply.get("channel_message", None)
        is_private_message = reply.get("private_message", None)
        is_command = reply.get("command", None)
        is_kill = reply.get("kill", None)
        is_get_status = reply.get("get_status", None) #voir si le gars est pas dans la liste actuelle, ajouter le bouton
        is_get_joined = reply.get("get_joined", None)
        is_join = reply.get("join", None)

        print(reply) #debug

        if is_register:
            return reply.get("register"), reply.get("ban", False), reply.get("kick", False) #True / False si bien registered ou pas

        elif is_login:
            is_logged = reply.get("login", False)
            is_banned = reply.get("ban", False)
            kick_time = reply.get("kick", False)
            need_register = reply.get("need_register", False)
            already_logged = reply.get("already_logged", False)

            return is_logged, is_banned, kick_time, need_register, already_logged

        elif is_channel_message:
            message = is_channel_message
            sender = reply.get("user", None)
            channel_name = reply.get("channel", None)
            self.cache[channel_name].append(f"{sender}> {message}")
            print(f"last item {self.last_item_clicked}, channel_name {channel_name}")
            if self.last_item_clicked == channel_name:
                print("append")
                self.show_message_box.appendPlainText(f"{sender}> {message}")


        elif is_private_message:
            message = is_private_message
            sender = reply.get("user", None)
            if not self.cache.get("sender", False):
                self.cache[sender] = []
            self.cache[sender].append(f"{sender}> {message}")

            if self.last_item_clicked == sender:
                self.show_message_box.appendPlainText(f"{sender}> {message}")

        elif is_command:
            if is_command == "Not allowed":
                QMessageBox.warning(self, "Erreur Commande", "Tu n'as pas le droit d'effectuer une commande")
            else:
                QMessageBox.information(self, "Info Commande", f"Votre commande a été effectué \n réponse du serveur : {is_command}")

        elif is_kill:
            if is_command == "Not allowed":
                QMessageBox.warning(self, "Erreur Kill", "Tu n'as pas le droit de kill le serveur")
            else:
                QMessageBox.information(self, "Kill", f"Le serveur doit s'arrêter")
                self.close_app()

        elif is_get_status:
            del is_get_status[self.username]
            print(self.last_item_clicked)
            if self.refresh and self.is_mp_btn_clicked:
                self.setup_private_msg()
                self.user_status = is_get_status
                self.refresh = False

            elif not self.is_mp_btn_clicked and is_get_status != self.user_status:
                self.user_status = is_get_status
                self.refresh = True

            elif self.is_mp_btn_clicked and is_get_status != self.user_status:
                self.user_status = is_get_status
                self.setup_private_msg()


            for user in self.user_status:
                if not self.cache.get("user", None):
                    self.cache[user] = []

            # del is_get_status[self.username]
            # self.user_status = is_get_status
            # if self.user_status.get(self.last_item_clicked, False) or self.is_mp_btn_clicked:
            #     #l'user est dans la section private msg donc il faut update les boutons
            #     self.setup_private_msg()


        elif is_get_joined:
            dict = reply.get("dict")
            for channel, status in dict.items():
                self.channels[channel] = status

        elif is_join:
            channel_name = reply.get("channel_name")
            status = "accepté" if reply.get("status") == "accept" else "refusé"
            self.new_status[channel_name] = status
            self.channels[channel_name] = reply.get("status")
            Thread(target=self.new_channel_msg, args=(channel_name, status)).start()
            # QMessageBox.information(self, f"Demande Channel {channel_name}",f"Votre demande pour le channel {channel_name} a été {status}")

        return False, False, False, False, False


    def handle_send_msg(self):
        msg = self.send_message_box.text()
        self.send_message_box.clear()
        print(self.last_item_clicked, self.is_mp_btn_clicked, self.cache)
        if self.last_item_clicked:
            if self.is_mp_btn_clicked:
                self.cache[self.last_item_clicked].append(f"moi> {msg}")
                self.show_message_box.appendPlainText(f"moi> {msg}")
                if self.user_status.get(self.last_item_clicked) != "deconnected":
                    self.s.send(str.encode(
                        json.dumps({'private_message': msg, "user": self.username, "other_user": self.last_item_clicked})))

            else:
                self.s.send(str.encode(json.dumps({'channel_message': msg, "user": self.username, "channel": self.last_item_clicked})))
                self.cache[self.last_item_clicked].append(f"moi> {msg}")
                self.show_message_box.appendPlainText(f"moi> {msg}")




    def new_channel_msg(self, channel_name, status):
        QMessageBox.information(self, f"Demande Channel {channel_name}",
                                f"Votre demande pour le channel {channel_name} a été {status}")







    def handle_login(self):
        "ici c'est seulement la logique de login / register"

        # check si username n'a pas de caractere spéciaux, espace etc etc, pareil pour le mdp

        username = self.username_line_edit_login.text()

        if not username:
            return QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom d'utilisateur.")
        elif len(username) < 3:
            return QMessageBox.warning(self, "Erreur", "Le nom d'utilisateur doit contenir au moins 3 caractères.")
        elif len(username) > 20:
            return QMessageBox.warning(self, "Erreur", "Le nom d'utilisateur doit contenir moins de 20 caractères.")

        password = self.password_line_edit_login.text()

        if not password:
            return QMessageBox.warning(self, "Erreur", "Veuillez entrer un password.")
        elif len(password) < 3:
            return QMessageBox.warning(self, "Erreur", "Le password doit contenir au moins 3 caractères.")
        elif len(password) > 20:
            return QMessageBox.warning(self, "Erreur", "Le password doit contenir moins de 20 caractères.")

        if self.is_login_page:
            "il n'a pas switch sur la page de register, il veut donc se log"
           # __reply = self.s.recv(1024).decode() je crois pas besoin de cette ligne, je crois que ca sert a rien d'envoyer un msg etc etc
            __reply = True
            if __reply:

                self.s.send(str.encode(json.dumps({'login': True, "user": username, "password": password})))
                print("sent")
                __reply = self.s.recv(1024).decode()
                reply = json.loads(__reply)

                is_logged, is_banned, kick_time, need_register, already_logged = self.handle_reply(reply)

                if is_logged:
                    t = Thread(target=self.receive_msg, args=(), name="receive_socket_msg").start()
                    self.thread.append(t)
                    t = Thread(target=self.get_status, args=(), name="get_status").start()
                    self.thread.append(t)
                    self.s.send(str.encode(json.dumps({'get_joined': True, "user": username})))
                    self.stackedWidget.setCurrentIndex(1)
                    self.setWindowTitle(f"Chat APP | Connecté en tant que : {username}")
                    self.logged = True
                    self.username = username
                    self.set_status()
                elif already_logged:
                    return QMessageBox.warning(self, "Erreur", "Ton compte est déjà connecté sur une autre machine !")
                elif is_banned:
                    QMessageBox.warning(self, "Erreur", "Ton ip ou ton username est banni !")
                    self.close_app()
                    return
                elif kick_time:
                    QMessageBox.warning(self, "Erreur", f"Ton ip ou ton username est kick jusqu'au {kick_time}!")
                    self.close_app()
                    return
                elif not is_logged and need_register:
                    return QMessageBox.warning(self, "User Inexistant",f"Tu as besoin de te register, aucun compte existe au nom d'{username}")
                elif not is_logged and not need_register:
                    return QMessageBox.warning(self, "User / mdp incorrect",f"Cette combinaison d'username / mdp n'est pas la bonne, réessaye !")
                else:
                    return print("Aucune idée du soucis")

            else:
                "erreur avec le serv"
        else:
            "il veut se register"
            #__reply = self.s.recv(1024).decode()
            __reply = True
            if __reply:
                self.s.send(str.encode(json.dumps({'register': True, "user": username, "password": password})))
                __reply = self.s.recv(1024).decode()
                reply = json.loads(__reply)
                is_registered, is_ban, kick_time = self.handle_reply(reply)
                print(is_registered, is_ban, kick_time)
                if is_registered and not is_ban and not kick_time:
                    return QMessageBox.information(self, "Register", "Vous avez bien été enregistré")
                elif not is_registered and not is_ban and not kick_time:
                    return QMessageBox.warning(self, "User Existant",f"L'username : {username} existe déjà")
                elif not is_registered and not is_ban and kick_time:
                    QMessageBox.warning(self, "Erreur", f"Ton ip ou ton username est kick jusqu'au {kick_time}!")
                    self.close_app()
                    return
                else:
                    QMessageBox.warning(self, "Erreur", "Ton ip ou ton username est banni !")
                    self.close_app()
                    return



    def switch_register_login(self):
        if self.is_login_page:
            self.btn_switch_to_register.setText("LOGIN PAGE")
            self.btn_submit_login.setText("SUBMIT REGISTER")
            self.username_label_login.setText("NEW USERNAME")
            self.password_label_login.setText("NEW PASSWORD")
            self.is_login_page = False
            self.setWindowTitle("Register page")
        else:
            self.btn_switch_to_register.setText("REGISTER PAGE")
            self.btn_submit_login.setText("SUBMIT LOGIN")
            self.username_label_login.setText("USERNAME")
            self.password_label_login.setText("PASSWORD")
            self.is_login_page = True
            self.setWindowTitle("Login page")



    def handle_btn_msg(self, item):
        # if self.new_status:
        #     for channel, status in self.new_status.items():
        #         info_box = QMessageBox()
        #         info_box.setIcon(QMessageBox.Information)
        #         info_box.setText(f"Votre demande pour le channel {channel} a été {status}")
        #         info_box.setWindowTitle(f"Demande Channel {channel}",)
        #         info_box.setStandardButtons(QMessageBox.Ok)
        #         result = info_box.exec_()
        #         if result == QMessageBox.Ok:
        #             pass
        #         del self.new_status[channel]
        #           bloque le code et fait crash le client

        if self.last_item_clicked != item.text().split("[")[0] and not self.is_mp_btn_clicked:
            if not self.channels.get(item.text().split("[")[0], False):
                #l'user n'a pas fait sa demande
                self.last_item_clicked = None
                message_box = QMessageBox()
                message_box.setWindowTitle("Demande")
                message_box.setText(f"Voulez-vous faire la demande pour rejoindre le channel : {item.text().split('[')[0]}")
                dmd_btn = message_box.addButton("Faire la demande", QMessageBox.AcceptRole)
                cancel_btn = message_box.addButton("Annuler", QMessageBox.RejectRole)
                message_box.exec_()
                if message_box.clickedButton() == dmd_btn:
                    self.channels[item.text().split("[")[0]] = "pending"
                    print(self.channels)
                    self.s.send(str.encode(json.dumps({'join': True, "user": self.username, "channel": item.text().split("[")[0]})))
                    return
                elif message_box.clickedButton() == cancel_btn:
                    return

            elif self.channels.get(item.text().split("[")[0], False) == "pending":
                self.last_item_clicked = None
                return QMessageBox.information(self, f"Demande channel {item.text().split('[')[0]}", f"Votre demande pour le channel {item.text().split('[')[0]} est en attente, il faut que le serveur accepte votre demande !")

            elif self.channels.get(item.text().split("[")[0], False) == "refuse":
                self.last_item_clicked = None
                return QMessageBox.Warning(self, f"Demande channel {item.text().split('[')[0]}", f"Votre demande pour le channel {item.text().split('[')[0]} à été refusé, vous ne pourrez pas avoir accès à ce channel")

            else:
                self.show_message_box.setPlainText("\n".join(self.cache[item.text().split("[")[0]]))
                self.last_item_clicked = item.text().split("[")[0]
                print("else", item.text().split("[")[0], self.last_item_clicked)
        elif self.last_item_clicked != item.text().split("[")[0] and self.is_mp_btn_clicked:
            self.last_item_clicked = item.text().split("[")[0]



    def btn_channel_clicked(self):
        if not self.is_mp_btn_clicked:
            return
        self.setup_public_msg()
        self.is_mp_btn_clicked = False
    def btn_private_clicked(self):
        if self.is_mp_btn_clicked:
            return
        self.setup_private_msg()
        self.is_mp_btn_clicked = True



    def bind_socket(self):
        self.s = socket.socket()
        try:
            self.s.connect((self.ip, self.port))
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error connecting with the server, closing App when you click on button")
            msg.setInformativeText(f'{e}')
            msg.setWindowTitle("Error")
            msg.exec_()
            self.close_app()



    def setup_public_msg(self):
        self.list_message_box.clear()
        self.show_message_box.clear()


        for channel in self.channels:
            item = QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(channel)
            self.list_message_box.addItem(item)

    def setup_private_msg(self):
        self.list_message_box.clear()
        self.show_message_box.clear()

        for user, status in self.user_status.items():
            item = QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(f"{user} [{status.upper()}]")
            self.list_message_box.addItem(item)


    def receive_msg(self):
        while self.is_running:
            try:
                __reply = self.s.recv(1024).decode()
                reply = json.loads(__reply)
                print(reply)
                is_logged, is_banned, kick_time, need_register, already_logged = self.handle_reply(reply)
                if is_banned:
                    QMessageBox.warning(self, "Erreur", "Ton ip ou ton username est banni !")
                    self.close_app()
                    return
                elif kick_time:
                    QMessageBox.warning(self, "Erreur", f"Ton ip ou ton username est kick jusqu'au {kick_time}!")
                    self.close_app()
                    return
                else:
                    pass
            except (ConnectionAbortedError, TypeError):
                pass




    def close_app(self):
        self.is_running = False
        try:
            # if self.logged:
            #     self.set_status(status="deconnected")
            if self.username: self.s.send(str.encode(json.dumps({'close': True, "user": self.username})))
            else: self.s.send(str.encode(json.dumps({'close': True})))
            self.s.close()
        except:
            pass
        QApplication.closeAllWindows()
        sys.exit()

    def set_status(self, status="connected"):
        self.s.send(str.encode(json.dumps({'set_status': status, "user": self.username})))

    def get_status(self):
        while self.is_running:
            self.s.send(str.encode(json.dumps({'get_status': True, "user": self.username})))
            sleep(5)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(ip="192.168.1.19",port=6530)
    #window.show()
    app.exec()