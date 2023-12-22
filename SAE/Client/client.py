
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSpacerItem, QMessageBox, QSizePolicy, QLabel, QLineEdit, QPushButton, QMainWindow, QFrame, QVBoxLayout, QStackedWidget, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt5 import QtGui, QtCore
from threading import Thread
import socket
import json


class MainWindow(QMainWindow):
    def __init__(self, ip:str, port:int):
        super().__init__()

        self.is_running = True
        self.is_mp_btn_clicked = False
        self.is_public_btn_clicked = False
        self.ip = ip
        self.port = port
        self.thread = []


        self.resize(800, 700)
        self.setWindowTitle("Login / Logout")

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

        self.login_layout.addWidget(self.username_line_edit_login, 1, 1, 1, 1)
        self.login_layout.addWidget(self.username_label_login, 0, 0, 1, 1)
        self.login_layout.addWidget(self.password_line_edit_login, 0, 1, 1, 1)
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

        self.show_message_box = QLineEdit(self.widget_3)
        self.show_message_box.setMaximumSize(QtCore.QSize(16777215, 10000))
        self.show_message_box.setText("")
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
#        t = Thread(target=self.receive_msg, args=(), name="receive_socket_msg").start()
#        self.thread.append(t)


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
        self.show_message_box.setText("")

        channels = ["Général", "Blabla", "Comptabilité", "Informatique", "Marketing"]

        for channel in channels:
            item = QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(channel)
            self.list_message_box.addItem(item)

    def receive_msg(self):
        ...


    def close_app(self):
        self.is_running = False
        try:
            self.s.send(str.encode(json.dumps({'close': True})))
            self.s.close()
        except:
            pass
        QApplication.closeAllWindows()
        sys.exit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(ip="1",port=9999)
    #window.show()
    app.exec()