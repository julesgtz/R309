from PyQt5.QtWidgets import QApplication, QComboBox,QWidget,QGridLayout,QLabel,QLineEdit,QPushButton, QMainWindow
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400,200)
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

        self.conversion_text = QLabel("Conversion")
        self.result = QLineEdit("")
        self.result.setReadOnly(True)
        self.unite2 = QLabel("K")

        grid.addWidget(self.temperature_text, 0, 0)
        grid.addWidget(self.text, 0, 1)
        grid.addWidget(self.unite1, 0, 2)

        grid.addWidget(self.convertir, 1,1)
        grid.addWidget(self.set_conversion, 1,3)

        grid.addWidget(self.conversion_text, 2, 0)
        grid.addWidget(self.result, 2, 1)
        grid.addWidget(self.unite2, 2, 2)



        self.convertir.clicked.connect(self.__convert)
        self.setWindowTitle("Conversion de Température")


    def __get_conversion_type(self):
        return True if self.set_conversion.currentText() == "K -> °C" else False




    def __convert(self):
        is_good = self.__value_checker()
        t = self.text.text()
        self.bonjour.setText(f"Bonjour {t}")


    def __value_checker(self, val, unite):
        if unite == "C":
            return False if val <=273.15 else True
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