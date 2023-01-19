import json

from PyQt6.QtWidgets import (QCheckBox, QComboBox, QLineEdit)

class Parameter:

    def __init__(self):
        self.Unique_id = -1
        self.GUI_id = -1
        self.DT_id = -1
        self.CSV_text = ''
        self.DataFormat = ''
        self.row = 0
        self.delimiter = ''


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class ParameterDialog(Parameter):

    def __init__(self, parameter: Parameter):
        super().__init__()
        # self.Unique_id = -1
        self.GUI_id = parameter.GUI_id
        self.DT_id = parameter.DT_id
        self.CSV_text = parameter.CSV_text
        self.DataFormat = parameter.DataFormat
        self.row = parameter.row
        self.delimiter = parameter.delimiter
        self.checkBoxChecked = False
        self.CheckBox = QCheckBox()
        self.CSVLineEdit = QLineEdit()
        self.DataTypeComboBox = QComboBox()
        self.DelimiterLineEdit = QLineEdit()
