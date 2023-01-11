import json

class parameter_transmission:

    GUI_id = int
    DT_id = int
    CSV_text = str
    DataFormat = str
    row = int

    def __init__(self):
        self.GUI_id = -1
        self.DT_id = -1
        self.CSV_text = ""
        self.DataFormat = ""
        self.row = 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)