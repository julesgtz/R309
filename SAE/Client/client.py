from PyQt5.QtWidgets import QApplication, QComboBox,QWidget,QGridLayout,QLabel,QLineEdit,QPushButton, QMainWindow, QMessageBox

class Client(QMainWindow):
    def __init__(self, ip:str, port: int):
        super().__init__()
        self.ip = ip
        self.port = port

