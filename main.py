import sys
import communication
import gui

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
# Main File zum Starten der GUI

# from qt_material import apply_stylesheet

app = QtWidgets.QApplication(sys.argv)
 
# apply_stylesheet(app, theme='dark_cyan.xml')

gui_main = gui.MainWindow()
gui_main.showGUI()
app.exec()