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
        """getUEBsettings SCPI-Kommando für Parameterabfrage erstellen

        Returns:
            String: SCPI-Kommando
        """        
        return (self.UEBREADY + self.CARRIAGE_RETURN)

    def setUEBSoftstartEnable(self, value):
        """setUEBSoftstartEnable SCPI-Kommando für Softstarteinstellung erstellen

        Args:
            value (Integer): 0 aus, 1 an

        Returns:
                String: SCPI-Kommando
        """        
        if(value):
            value = '1'
        else:
            value = '0'
        return (self.UEB + self.DELIMITER_PARTMESSAGE + self.SOFTSTART + self.DELIMITER_PARTMESSAGE + self.D_ENABLE + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)

    def setUEBSoftstartDuration(self, value):
        """setUEBSoftstartDuration Erstellt das SCPI-Kommando für die Softstartdauer

        Args:
            value (Float): Dauer in Sekunden

        Returns:
            String: SCPI-Kommando
        """        
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.SOFTSTART + self.DELIMITER_PARTMESSAGE  + self.DURATION + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + str(value) + self.CARRIAGE_RETURN)

    def setUEBThridHarmonic(self, value):
        """setUEBThridHarmonic Erstellt das SCPI-Kommando für die Dritte Harmonische

        Args:
            value (Integer): 0 aus, 1 an

        Returns:
            String: SCPI-Kommando
        """        
        if(value):
            value = '1'
        else:
            value = '0'        
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.CONFIG + self.DELIMITER_PARTMESSAGE  + self.TRDHARMONIC + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)

    def setUEBRotation(self, value):
        """setUEBRotation Erstellt das SCPI-Kommando für die Rotationsrichtung

        Args:
            value (Integer): Drehrichtung siehe Controllercode

        Returns:
            String: SCPI-Kommando
        """
        if(value):
            value = '1'
        else:
            value = '0'
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.CONFIG + self.DELIMITER_PARTMESSAGE  + self.ROTATION + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)

    def setUEBVBridge(self, value):
        """setUEBVBridge Erstellt das SCPI-Kommando für die Brückenspannung

        Args:
            value (Float): Spannung in Volt

        Returns:
            String: SCPI-Kommando
        """
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.PARAMETER + self.DELIMITER_PARTMESSAGE  + self.VCC + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + str(value) + self.CARRIAGE_RETURN)

    def setUEBVout(self, value):
        """setUEBVout Erstellt das SCPI-Kommando für die Ausgangsspannung

        Args:
            value (Float): Spannung in Volt

        Returns:
            String: SCPI-Kommando
        """
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.PARAMETER + self.DELIMITER_PARTMESSAGE  + self.VOUT + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + str(value) + self.CARRIAGE_RETURN)

    def setUEBFrequency(self, value):
        """setUEBFrequency Erstellt das SCPI-Kommando für die Frequenz

        Args:
            value (Float): Frequenz in Hertz

        Returns:
            String: SCPI-Kommando
        """
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.PARAMETER + self.DELIMITER_PARTMESSAGE  + self.FREQUENCY + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + str(value) + self.CARRIAGE_RETURN)

    def setUEBCurrent(self, value):
        """setUEBCurrent Erstellt das SCPI-Kommando für die Stromstärke

        Args:
            value (Float): Stromstärke in Ampere

        Returns:
            String: SCPI-Kommando
        """
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.PARAMETER + self.DELIMITER_PARTMESSAGE  + self.CURRENT + self.DELIMITER_PARTMESSAGE  + self.VALUE + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)

    def setUEBsettings(self, value):
        """setUEBsettings Erstellt das SCPI-Kommando für das Übernehmen der Einstellungen auf dem Controller

        Args:
            value (Integer): n.b.

        Returns:
            String: SCPI-Kommando
        """
        # if(value):
        #     value = '1'
        # else:
        #     value = '0'
        # return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.SYSTEM + self.DELIMITER_PARTMESSAGE  + self.D_ENABLE + self.DELIMITER_PARTMESSAGE + value + self.CARRIAGE_RETURN)
        return (self.UEB + self.DELIMITER_PARTMESSAGE  + self.SYSTEM + self.DELIMITER_PARTMESSAGE  + self.D_ENABLE + self.DELIMITER_PARTMESSAGE + str(value) + self.CARRIAGE_RETURN)


    def setDatatransmission(self):
        """setDatatransmission Erstellt das SCPI-Kommando für den Start einer großen Datenübertragung tbd!

        Returns:
            String: SCPI-Kommando
        """
        return (self.DATATRANSMISSION + self.DELIMITER_PARTMESSAGE + self.CONFIG + self.CARRIAGE_RETURN)

    def setDatatransmissionComplete(self, id):
        """setDatatransmissionComplete Erstellt das SCPI-Kommando für die Bestätigung über eine erfolgreiche Übertragung einer ID

        Args:
            id (Integer): ID der Übertragung

        Returns:
            String: SCPI-Kommando
        """
        return (self.DATATRANSMISSION + self.DELIMITER_PARTMESSAGE + self.COMPLETE + self.DELIMITER_PARTMESSAGE + str(id) + self.CARRIAGE_RETURN)

    def setDatatransmissionInit(self, id):
        """setDatatransmissionInit Erstellt das SCPI-Kommando für den Start einer ID Übertragung 

        Args:
            id (Integer): ID der Übertragung

        Returns:
            String: SCPI-Kommando
        """
        return (self.DATATRANSMISSION + self.DELIMITER_PARTMESSAGE + self.INIT + self.DELIMITER_PARTMESSAGE + str(id) + self.CARRIAGE_RETURN)













