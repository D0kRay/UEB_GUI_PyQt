from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6 import QtWidgets
import sys

def on_clicked():
    print("clicked")


def main():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(100, 200, 300, 300)
    win.setWindowTitle("PyQt GUI")

    text = QLabel(win)
    text.setText('Test String')
    text.move(50,50)

    btn1 = QtWidgets.QPushButton(win)
    btn1.setText("Click me!")
    btn1.clicked.connect(on_clicked)

    win.show()

    sys.exit(app.exec())

main()
   