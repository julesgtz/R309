from PyQt5.QtWidgets import QApplication, QComboBox,QWidget,QGridLayout,QLabel,QLineEdit,QPushButton, QMainWindow, QMessageBox
import sys
import socket
from time import sleep
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.all_val = []
        self.last_value = None

        self.setFixedSize(500,200)
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.fonction_text = QLabel("Fonction")
        self.fonction = QLineEdit("")

        self.val_min_text = QLabel("Valeur minimale")
        self.val_min = QLineEdit("")

        self.val_max_text = QLabel("Valeur maximale")
        self.val_max = QLineEdit("")

        self.pas_text = QLabel("Pas")
        self.pas = QLineEdit("")

        self.resultat_text = QLabel("Résultat")
        self.resultat = QLineEdit("")
        self.resultat.setReadOnly(True)

        self.calcul = QPushButton('Calcul', self)
        self.quitter = QPushButton('Quitter', self)

        grid.addWidget(self.fonction_text, 0, 0)
        grid.addWidget(self.fonction, 0, 1)

        grid.addWidget(self.val_min_text, 1,0)
        grid.addWidget(self.val_min, 1,1)

        grid.addWidget(self.val_max_text, 2, 0)
        grid.addWidget(self.val_max, 2, 1)

        grid.addWidget(self.pas_text, 3, 0)
        grid.addWidget(self.pas, 3, 1)

        grid.addWidget(self.resultat_text, 4, 0)
        grid.addWidget(self.resultat, 4, 1)

        grid.addWidget(self.calcul, 6, 0)
        grid.addWidget(self.quitter, 6, 1)



        self.calcul.clicked.connect(self.__calcul)
        self.quitter.clicked.connect(self.__quitter)

        self.setWindowTitle("mathlogsock_client")

    def __get_all_val(self):
        try:
            val_min = float(self.val_min.text())
        except Exception as e:
            return False, e
            # "renvoie erreur"

        try:
            val_max = float(self.val_max.text())
        except Exception as e:
            return False, e
            # "renvoie erreur"

        if val_max >= val_min:
            return False, "Valeur minimal > Valeur maximale"

        try:
            pas = float(self.pas.text())
        except Exception as e:
            return False, e

        if self.last_value:
            lval_min = self.last_value[0]
            lval_max = self.last_value[1]
            lpas = self.last_value[2]

            if lval_max == val_max and lval_min == val_min and lpas == pas:
                return True, False
            else:
                self.all_val = []

        current_number = val_min
        while current_number < val_max:
            self.all_val.append(current_number)
            current_number += pas
        else:
            self.all_val.append(val_max)

        self.last_value = [val_min, val_max, pas]

        return True, False


    def __log_socket(self):
        self.client = socket.socket()
        self.client.connect(("127.0.0.1", 6350))
        print("connected")
    def __quitter(self):
        self.__log_socket()
        self.client.send(str("arret").encode())
        self.client.close()
        QApplication.exit(0)
    def __calcul(self):
        self.__log_socket()
        good, error = self.__get_all_val()

        if not good and error:
            self.resultat.setText(error)

        if good and not error:
            if self.all_val:
                self.client.send(str(self.fonction.text()).encode())
                sleep(0.5)
                self.client.send(str(self.all_val[0]).encode())
                self.all_val.pop(0)
                reponse = self.client.recv(1024).decode()
                self.resultat.setText(reponse)
            else:
                self.resultat.setText("Vous avez deja la valeur max")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()