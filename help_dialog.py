from PyQt6.QtWidgets import (QLabel, QDialog, QSizePolicy, QVBoxLayout)
from ui_helpdialog import Ui_HelpDialog

class HelpDialog(QDialog, Ui_HelpDialog):

    def __init__(self, parent=None):
        super(HelpDialog, self).__init__(parent)
        self.setupUi(self)
        self.helpTextList = []
        self.rowlayout = QVBoxLayout()
        self.fillScrollBox()
        self.close_pushButton.clicked.connect(self.accept)

    def fillScrollBox(self):
        self.helpMessage = "readme.txt nicht gefunden"
        with open('readme.txt', 'r') as reader:
            self.helpMessage = (reader.read()).split('\n')
        for i in range(0, len(self.helpMessage)):
            text = QLabel()    
            sizePolicy = QSizePolicy()
            sizePolicy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
            text.setText(self.helpMessage[i])
            text.setSizePolicy(sizePolicy)
            text.setMinimumSize(40,15)
            self.rowlayout.addWidget(text)
            self.help_scrollAreaWidgetContents.setLayout(self.rowlayout)
