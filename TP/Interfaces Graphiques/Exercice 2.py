from PyQt5.QtWidgets import QApplication, QComboBox,QWidget,QGridLayout,QLabel,QLineEdit,QPushButton, QMainWindow, QMessageBox
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500,200)
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.temperature_text = QLabel("Température")
        self.text = QLineEdit("")
        self.unite1 = QLabel("°C")

        self.convertir = QPushButton("Convertir")
        self.set_conversion = QComboBox()
        self.set_conversion.addItems(["°C -> K", "K -> °C"])
        self.set_conversion.setFixedSize(150,20)

        self.conversion_text = QLabel("Conversion")
        self.result = QLineEdit("")
        self.result.setReadOnly(True)
        self.unite2 = QLabel("K")

        self.help = QPushButton('?', self)
        self.help.setFixedSize(25,25)

        grid.addWidget(self.temperature_text, 0, 0)
        grid.addWidget(self.text, 0, 1)
        grid.addWidget(self.unite1, 0, 2)

        grid.addWidget(self.convertir, 1,1)
        grid.addWidget(self.set_conversion, 1,3)

        grid.addWidget(self.conversion_text, 2, 0)
        grid.addWidget(self.result, 2, 1)
        grid.addWidget(self.unite2, 2, 2)

        grid.addWidget(self.help, 3, 4)



        self.convertir.clicked.connect(self.__convert)
        self.help.clicked.connect(self.__help)
        self.setWindowTitle("Conversion de Température")

    def __help(self):
        QMessageBox.information(self, 'Aide', 'Permet de convertir un nombre soit de Kelvin vers Celcius, soit de Celcius vers Kelvin')

    def __change_q_label(self, uni1, uni2):
        self.unite1.setText(uni1)
        self.unite2.setText(uni2)

    def __error(self, val):
        QMessageBox.information(self, 'Erreur', f"Veuillez entrer une valeur correcte, '{val}' n'en est pas une !")

    def __get_conversion_type(self):
        return True if self.set_conversion.currentText() == "K -> °C" else False

    def __convert(self):
        try:
            float(self.text.text())
        except:
            self.__error(self.text.text())
            return
        unite = "K" if self.__get_conversion_type() else "C"
        value = float(self.text.text())
        is_good = self.__value_checker(val=value, unite=unite)
        if is_good:
            uni1, uni2 = ("K", "°C") if self.set_conversion.currentText() == "K -> °C" else ("°C", "K")
            self.__change_q_label(uni1=uni1, uni2=uni2)
            self.result.setText(str(value + 273.15 if unite =="C" else value - 273.15))
        else:
            self.result.setText("")
            self.__error(self.text.text())



    def __value_checker(self, val: float, unite :str):
        if unite == "C":
            return False if val <= -273.15 else True
        elif unite == "K":
            return False if val < 0 else True
        else:
            return False
    def __actionQuitter(self):
        QApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()