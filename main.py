from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIcon
from qt_material import apply_stylesheet
from MainWindow import Ui_MainWindow
import sys

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)


app = QtWidgets.QApplication(sys.argv)

apply_stylesheet(app, theme='dark_teal.xml')

window = MainWindow()
window.setWindowIcon(QIcon("UEB_icon.png"))
window.setWindowTitle("UEB Tester")
window.show()
app.exec()