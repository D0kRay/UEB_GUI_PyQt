# Form implementation generated from reading ui file 'c:\Users\pasik\Documents\UEB_GUI_PyQt\UEB_GUI_PyQt\ui_helpdialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        HelpDialog.setObjectName("HelpDialog")
        HelpDialog.resize(863, 496)
        self.verticalLayoutWidget = QtWidgets.QWidget(HelpDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 861, 491))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.help_scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        self.help_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.help_scrollArea.setWidgetResizable(True)
        self.help_scrollArea.setObjectName("help_scrollArea")
        self.help_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.help_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 840, 457))
        self.help_scrollAreaWidgetContents.setObjectName("help_scrollAreaWidgetContents")
        self.help_scrollArea.setWidget(self.help_scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.help_scrollArea)
        self.close_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.close_pushButton.setObjectName("close_pushButton")
        self.verticalLayout.addWidget(self.close_pushButton)

        self.retranslateUi(HelpDialog)
        QtCore.QMetaObject.connectSlotsByName(HelpDialog)

    def retranslateUi(self, HelpDialog):
        _translate = QtCore.QCoreApplication.translate
        HelpDialog.setWindowTitle(_translate("HelpDialog", "Dialog"))
        self.close_pushButton.setText(_translate("HelpDialog", "Schliessen"))
