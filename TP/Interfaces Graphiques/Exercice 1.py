from PyQt5.QtWidgets import QApplication, QWidget,QGridLayout,QLabel,QLineEdit,QPushButton, QMainWindow
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300,150)
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        lab = QLabel("Saisir votre nom")
        self.text = QLineEdit("")
        self.bonjour = QLabel("")
        ok = QPushButton("Ok")
        quit = QPushButton("Quitter")

        grid.addWidget(lab, 0, 0)
        grid.addWidget(self.text, 1, 0)
        grid.addWidget(ok, 2, 0)
        grid.addWidget(self.bonjour, 3, 0)
        grid.addWidget(quit, 4,0)

        ok.clicked.connect(self.__actionOk)
        quit.clicked.connect(self.__actionQuitter)
        self.setWindowTitle("Une première fenêtre")
    def __actionOk(self):
        t = self.text.text()
        self.bonjour.setText(f"Bonjour {t}")
    def __actionQuitter(self):
        QApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()