from PyQt6.QtWidgets import (QLabel, QSizePolicy, QLineEdit, QDialog, QCheckBox, QComboBox, QHBoxLayout, QVBoxLayout)
from ui_parameter_dialog import Ui_TransmissionParameterDialog
from parameter import ParameterDialog, Parameter
from datatypes import DataTypes                             

class TransmissionDialog(QDialog, Ui_TransmissionParameterDialog):

    def __init__(self, parameterlist, parent=None):
        super(TransmissionDialog, self).__init__(parent)
        self.available_parameterList = []
        self.used_parameterlist = []
        self.dataTypesObj = DataTypes()
        for i in range(0, len(parameterlist)):
            self.available_parameterList.append(ParameterDialog(parameterlist[i]))
        self.setupUi(self)
        self.availableID_verticalLayout = QVBoxLayout()
        self.usedID_verticalLayout = QVBoxLayout()


        self.fillAvailableScrollBox()

        self.Cancel_pushButton.clicked.connect(self.cancelButtonClicked)
        self.OK_pushButton.clicked.connect(self.okButtonClicked)
        self.addNewUserID.clicked.connect(self.okButtonClicked)
        self.addToTransmittedScrollBox_pushButton.clicked.connect(self.fillUsedScrollBox)
        

    def okButtonClicked(self):
        """okButtonClicked Handler der OK Schaltfläche
        """
        for i in range(0, len(self.used_parameterlist)):
            self.used_parameterlist[i].CSV_text = self.used_parameterlist[i].CSVLineEdit.text()
            self.used_parameterlist[i].DataFormat = self.used_parameterlist[i].DataTypeComboBox.currentText()
            self.used_parameterlist[i].delimiter = self.used_parameterlist[i].DelimiterLineEdit.text()
        self.accept()
    
    def cancelButtonClicked(self):
        """cancelButtonClicked Handler der Abbrechen Schaltfläche
        """
        self.reject()
            

    def fillAvailableScrollBox(self):
        """fillAvailableScrollBox Ausfüllen der verfügbare ID ScrollBox
        """
        self.clearLayout(self.availableID_verticalLayout)
        for i in range(0, len(self.available_parameterList)):
            datatypes = self.dataTypesObj.getDataTypesAsList()
            parameterObj = self.available_parameterList[i]
            CheckBox = QCheckBox()
            csvLineEdit = QLineEdit()
            dataTypeComboBox = QComboBox()
            delimiterLineEdit = QLineEdit()
            sizePolicy = QSizePolicy()
            sizePolicy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
            CheckBox.setText(parameterObj.GUI_id)
            CheckBox.setSizePolicy(sizePolicy)
            CheckBox.setMinimumSize(40,30)
            csvLineEdit.setText(parameterObj.CSV_text)
            dataTypeComboBox.addItems(datatypes)
            delimiterLineEdit.setText(parameterObj.delimiter)
            rowlayout = QHBoxLayout()
            rowlayout.addWidget(CheckBox)
            rowlayout.addWidget(csvLineEdit)
            rowlayout.addWidget(dataTypeComboBox)
            rowlayout.addWidget(delimiterLineEdit)
            self.availableID_verticalLayout.addLayout(rowlayout)
            self.scrollAreaWidgetContents.setLayout(self.availableID_verticalLayout)
            parameterObj.CheckBox = CheckBox
            parameterObj.CSVLineEdit = csvLineEdit
            parameterObj.DataTypeComboBox  = dataTypeComboBox
            parameterObj.DelimiterLineEdit = delimiterLineEdit
            self.available_parameterList[i] = parameterObj


    def fillUsedScrollBox(self):
        """fillUsedScrollBox Ausfüllen der ausgewählten ID ScrollBox
        """
        self.used_parameterlist.clear()
        self.clearLayout(self.usedID_verticalLayout)
        for i in range(0, len(self.available_parameterList)):
            if(self.available_parameterList[i].CheckBox.isChecked()):
                parameterObj = self.available_parameterList[i]
                idLabel = QLabel()
                csvLabel = QLabel()
                datatypeLabel = QLabel()
                delimiterLabel = QLabel()
                sizePolicy = QSizePolicy()
                sizePolicy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                idLabel.setText(parameterObj.CheckBox.text())
                idLabel.setMinimumSize(40,30)
                idLabel.setSizePolicy(sizePolicy)
                csvLabel.setText(parameterObj.CSVLineEdit.text())
                datatypeLabel.setText(parameterObj.DataTypeComboBox.currentText())
                delimiterLabel.setText(parameterObj.DelimiterLineEdit.text())
                rowlayout = QHBoxLayout()
                rowlayout.addWidget(idLabel)
                rowlayout.addWidget(csvLabel)
                rowlayout.addWidget(datatypeLabel)
                rowlayout.addWidget(delimiterLabel)
                self.usedID_verticalLayout.addLayout(rowlayout)
                self.scrollAreaWidgetContents_2.setLayout(self.usedID_verticalLayout)
                self.used_parameterlist.append(parameterObj)

    def createNewParameter(self):
        """createNewParameter Öffnen des Dialogs für neue Paramter IDs
        """
        #open extra dialog
        self.fillAvailableScrollBox()

    def clearLayout(self, layout):
        """clearLayout Leeren des übergebenen Layouts

        Args:
            layout (Layout): Layout welches geleert werden soll
        """
        if layout is not None:
            while layout.count():
                childlayout = layout.takeAt(0)
                if childlayout.widget() is not None:
                    childlayout.widget().deleteLater()
                elif childlayout.layout() is not None:
                    self.clearLayout(childlayout.layout())

    def getParameterList(self):
        """getParameterList Gibt die Parameter zurück, welcher der Benutzer ausgewählt hat.  

        Returns:
            List: Liste mit Parameterobjekten
        """
        parameterlist = []
        for i in range(0, len(self.used_parameterlist)):
            parameter = Parameter()
            parameter.GUI_id = self.used_parameterlist[i].GUI_id
            parameter.DT_id = self.used_parameterlist[i].DT_id
            parameter.CSV_text = self.used_parameterlist[i].CSV_text
            parameter.DataFormat = self.used_parameterlist[i].DataFormat
            parameter.delimiter = self.used_parameterlist[i].delimiter
            parameter.row = self.used_parameterlist[i].row
            parameterlist.append(parameter)

        return parameterlist
                

