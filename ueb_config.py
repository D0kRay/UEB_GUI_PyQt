import json

class ueb_config:

    # frequency = 10
    # v_Bridge = 20
    # v_Reference = 60
    # softstartDuration = 1.0
    # # overCurrentThreshold = 
    # pwmFrequency = 20000
    # rotationDirection = 1
    # thridHarmonic = False
    # enableSoftstarter = False

    def __init__(self):
        self.status = 0
        self.frequency = 50
        self.v_Bridge = 20
        self.v_Reference = 60
        self.softstartDuration = 1.0
        self.overCurrentThreshold = 20
        self.pwmFrequency = 20000
        self.rotationDirection = 1
        self.thridHarmonic = False
        self.enableSoftstarter = False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


