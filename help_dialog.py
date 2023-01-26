from PyQt6.QtWidgets import (QLabel, QScrollArea, QPushButton, QDialog, QCheckBox, QComboBox, QHBoxLayout, QVBoxLayout)
from ui_helpdialog import Ui_HelpDialog

class HelpDialog(QDialog, Ui_HelpDialog):

    def __init__(self, parent=None):
        super(HelpDialog, self).__init__(parent)
        self.setupUi(self)
        self.scrollArea = QScrollArea()
        self.close_pushButton = QPushButton()
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.close_pushButton)
        # self.help_scrollArea.setWidgetResizable(True)
        # self.usedID_verticalLayout = QVBoxLayout()
        # self.fillScrollBox()
        # self.close_pushButton.clicked.connect(self.accept)

    def fillScrollBox(self):
        self.helpMessage = "readme.txt nicht gefunden"
        with open('readme.txt', 'r') as reader:
            self.helpMessage = reader.read()
        idLabel = QLabel()    
        # sizePolicy = QSizePolicy()
        # sizePolicy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
        idLabel.setText(self.helpMessage)
        # idLabel.setMinimumSize(500,500)
        # idLabel.setSizePolicy(sizePolicy)
        self.usedID_verticalLayout.addWidget(idLabel)
        self.help_scrollArea.setLayout(self.usedID_verticalLayout)
