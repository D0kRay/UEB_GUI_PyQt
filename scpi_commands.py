class scpi_commands:

    def __init__(self):
        self.UEBREADY = "?"
        self.UEB = "UEB"
        self.SOFTSTART = "SOFTSTART"
        self.DURATION = "DUR"
        self.VALUE = "VALUE"
        self.TRDHARMONIC = "TRDHARM"
        self.ROTATION = "ROT"
        self.VCC = "VCC"
        self.VOUT = "VOUT"
        self.CONFIGURATION = "CONFIG"
        self.PARAMETER = "PARAM"
        self.D_ENABLE = "ENAB"
        self.FREQUENCY = "FREQ"
        self.CURRENT = "CURR"
        self.PERIPHERAL = "PERI"
        self.ADC = "ADC"
        self.SYSTEM = "SYST"
        self.CHANNEL = "CH"
        self.RES = "RES"
        self.DEVICE = "DEV"
        self.STAT = "STAT"
        self.CONFIG = "CONFIG"
        self.THRES = "THRES"
        self.LOS = "LOS"
        self.DOS = "DOS"
        self.LOT = "LOT"
        self.OVERRANGE = "OVERRANGE"
        self.MISMATCH = "MISMATCH"
        self.D_RESET = "RESET"
        self.MIN = "MIN"
        self.MAX = "MAX"
        self.HIGH = "HIGH"
        self.LOW = "LOW"
        self.EXCITATION = "EX"
        self.PHASELOCKRANGE = "PLR"
        self.HYSTERESIS = "HYST"
        self.ENCODER = "ENCOD"
        self.RDC = "RDC"
        self.INKREMENTAL = "INKR"
        self.DATATRANSMISSION = "DT"
        self.COMPLETE = "COMPLETE"
        self.INIT = "INIT"
        self.DELIMITER_FULLMESSAGE = ""
        self.DELIMITER_PARTMESSAGE = ":"
        self.CARRIAGE_RETURN = "\r"

    def getUEBsettings(self):
        return (self.UEBREADY + self.CARRIAGE_RETURN)

    def setUEBSoftstartEnable(self, value):
        if(value):
            value = '1'
        else:
            value = '0'
        return (self.UEB + self.DELIMITER_PARTMESSAGE + self.SOFTSTART + self.DELIMITER_PARTMESSAGE + self.D_ENABLE + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)

    def setUEBSoftstartDuration(self, value):
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.SOFTSTART + self.DELIMITER_PARTMESSAGE  + self.DURATION + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + str(value) + self.CARRIAGE_RETURN)

    def setUEBThridHarmonic(self, value):
        if(value):
            value = '1'
        else:
            value = '0'        
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.CONFIG + self.DELIMITER_PARTMESSAGE  + self.TRDHARMONIC + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)

    def setUEBRotation(self, value):
        if(value):
            value = '1'
        else:
            value = '0'
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.CONFIG + self.DELIMITER_PARTMESSAGE  + self.ROTATION + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)

    def setUEBVBridge(self, value):
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.PARAMETER + self.DELIMITER_PARTMESSAGE  + self.VCC + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + str(value) + self.CARRIAGE_RETURN)

    def setUEBVout(self, value):
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.PARAMETER + self.DELIMITER_PARTMESSAGE  + self.VOUT + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + str(value) + self.CARRIAGE_RETURN)

    def setUEBFrequency(self, value):
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.PARAMETER + self.DELIMITER_PARTMESSAGE  + self.FREQUENCY + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + str(value) + self.CARRIAGE_RETURN)

    def setUEBCurrent(self, value):
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.PARAMETER + self.DELIMITER_PARTMESSAGE  + self.CURRENT + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)

    def setUEBsettings(self, value):
        if(value):
            value = '1'
        else:
            value = '0'
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.SYSTEM + self.DELIMITER_PARTMESSAGE  + self.D_ENABLE + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)

    def setDatatransmission(self):
        return (self.DATATRANSMISSION + self.DELIMITER_PARTMESSAGE + self.CONFIG + self.CARRIAGE_RETURN)

    def setDatatransmissionComplete(self, id):
        return (self.DATATRANSMISSION + self.DELIMITER_PARTMESSAGE + self.COMPLETE + self.DELIMITER_PARTMESSAGE + id[2:] + self.CARRIAGE_RETURN)

    def setDatatransmissionInit(self, id):
        return (self.DATATRANSMISSION + self.DELIMITER_PARTMESSAGE + self.INIT + self.DELIMITER_PARTMESSAGE + str(id) + self.CARRIAGE_RETURN)













