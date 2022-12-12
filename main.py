import sys
import communication
import gui

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from qt_material import apply_stylesheet

app = QtWidgets.QApplication(sys.argv)

apply_stylesheet(app, theme='dark_cyan.xml')

gui0 = gui.MainWindow()
gui0.showGUI()

com = communication.Communication()
com.getComPorts()

app.exec()