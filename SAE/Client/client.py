
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
        self.ip = ip
        self.port = port
        self.thread = []
        self.user_status = {"Cheval":"deco","marie":"connected","test":"test"}
        self.username = ""
        self.cache = {"Général": ["moi -> test", "charles -> awee"], "Blabla": ["salut"], "Comptabilité": [], "Informatique": [], "Marketing": []}
        #ajoute au buffer des qu'un msg est recu (pour les channels, check si l'user a bien acces aux channels)
        self.last_item_clicked = None
        self.channels_join = {} # nom du channel : status ( accepted / pending / refused )

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

        #self.bind_socket()
#        t = Thread(target=self.receive_msg, args=(), name="receive_socket_msg").start()
#        self.thread.append(t)
        #t = Thread(target=self.get_status, args=(), name="get_status").start()
        #self.thread.append(t)

        self.private_msg_btn.clicked.connect(self.btn_private_clicked)
        self.channel_msg_btn.clicked.connect(self.btn_channel_clicked)
        self.list_message_box.itemClicked.connect(self.handle_btn_msg)
        self.btn_submit_login.clicked.connect(self.handle_login)
        self.btn_switch_to_register.clicked.connect(self.switch_register_login)

    def closeEvent(self, event):
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

        print(reply) #debug

        if is_register:
            return reply.get("register") #True / False si bien registered ou pas

        elif is_login:
            is_logged = reply.get("login", False)
            is_banned = reply.get("ban", False)
            kick_time = reply.get("kick", False)
            need_register = reply.get("need_register", False)
            return is_logged, is_banned, kick_time, need_register

        elif is_channel_message:
            message = is_channel_message
            sender = reply.get("user", None)
            channel_name = reply.get("channel", None)
            self.cache[channel_name].append(f"{sender}> {message}")

            if self.last_item_clicked == channel_name:
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
            ...



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
            __reply = self.s.recv(1024).decode()
#            __reply = True
            if __reply:

                self.s.send(str.encode(json.dumps({'login': True, "user": username, "password": password})))
                __reply = self.s.recv(1024).decode()
                reply = json.loads(__reply)

                is_logged, is_banned, kick_time, need_register = self.handle_reply(reply)

                if is_logged:
                    self.stackedWidget.setCurrentIndex(1)
                    self.setWindowTitle(f"Chat APP | Connecté en tant que : {username}")
                    self.username = username
                elif is_banned:
                    return QMessageBox.Critical(self, "Erreur", "Ton ip ou ton username est banni !")
                elif kick_time:
                    return QMessageBox.Critical(self, "Erreur", f"Ton ip ou ton username est kick jusqu'au {kick_time} !")
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
            __reply = self.s.recv(1024).decode()
            #            __reply = True
            if __reply:
                self.s.send(str.encode(json.dumps({'register': True, "user": username, "password": password})))
                __reply = self.s.recv(1024).decode()
                reply = json.loads(__reply)
                is_registered = self.handle_reply(reply)
                if is_registered:
                    return QMessageBox.information(self, "Register", "Vous avez bien été enregistré")
                else:
                    return QMessageBox.warning(self, "User Existant",f"L'username : {username} existe déjà")



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
        if self.last_item_clicked != item.text().split("[")[0]:

            self.show_message_box.setPlainText("\n".join(self.cache[item.text().split("[")[0]]))
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

        channels = ["Général", "Blabla", "Comptabilité", "Informatique", "Marketing"]

        for channel in channels:
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
            __reply = self.s.recv(1024).decode()
            reply = json.loads(__reply)
            self.handle_reply(reply)




    def close_app(self):
        self.is_running = False
        try:
            self.set_status(status="deconnected")
            self.s.send(str.encode(json.dumps({'close': True})))
            self.s.close()
        except:
            pass
        QApplication.closeAllWindows()
        sys.exit()

    def set_status(self, status="connected"):
        self.s.send(str.encode(json.dumps({'status': status, "user": self.username})))

    def get_status(self):
        while self.is_running:
            self.s.send(str.encode(json.dumps({'get_status': True, "user": self.username})))
            sleep(5)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(ip="1",port=9999)
    #window.show()
    app.exec()