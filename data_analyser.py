import os
import struct

from data_content import DataContent
from datatypes import DataTypes
from parameter import Parameter


class DataAnalyser():

    def __init__(self):
        self.inData = []
        self.filePath = ''
        self.dataTypes = DataTypes()
        self.old_processedData = []

    def processData(self, data, parameter, filePath):
        """processData Verarbeitet die Daten anhand der Paramtereinstellungen und speichert diese im übergebenen Dateipfad

        Args:
            data (List): Liste mit Daten
            parameter (List): Liste mit Parametern zu den Daten
            filePath (String): Pfad zur Datenspeicherung
        """
        self.filePath = filePath
        datastring = ''
        splited_data = []
        for i in range(0, len(data)):
            datastring = datastring + data[i].Data
        if(self.dataTypes.str in parameter.DataFormat or len(parameter.DataFormat) == 0):
            decodedString = ''
            try:
                decodedString = bytes.fromhex(datastring).decode('ascii')
            except:
                print("Nicht decodierbarer Hex String für ASCII Umwandlung")

            if(len(parameter.delimiter) != 0):
                splited_data = decodedString.split(parameter.delimiter)
            else:
                splited_data.append(decodedString)
        else: 
            #data must be hex !!!
            if(self.dataTypes.uint8_t in parameter.DataFormat):
                modulo = len(datastring) % 2
                for i in range(0, (len(datastring)-modulo), 2):
                # for i in range(0, len(datastring), 2):
                    splited_data.append(str(int(datastring[i:i+2], 16)))
            elif(self.dataTypes.uint16_t in parameter.DataFormat):
                modulo = len(datastring) % 4
                for i in range(0, (len(datastring)-modulo), 4):
                # for i in range(0, len(datastring), 4):
                    splited_data.append(str(int(datastring[i:i+4], 16)))
            elif(self.dataTypes.uint32_t in parameter.DataFormat):
                modulo = len(datastring) % 8
                for i in range(0, (len(datastring)-modulo), 8):
                # for i in range(0, len(datastring), 8):
                    splited_data.append(str(int(datastring[i:i+8], 16)))
            elif(self.dataTypes.int8_t in parameter.DataFormat):
                modulo = len(datastring) % 2
                for i in range(0, (len(datastring)-modulo), 2):
                # for i in range(0, len(datastring), 2):
                    splited_data.append(str(struct.unpack('<b', bytes.fromhex(datastring[i:i+2]))[0]))
            elif(self.dataTypes.int16_t in parameter.DataFormat):
                modulo = len(datastring) % 4
                for i in range(0, (len(datastring)-modulo), 4):
                # for i in range(0, len(datastring), 4):
                    splited_data.append(str(struct.unpack('<h', bytes.fromhex(datastring[i:i+4]))[0]))
            elif(self.dataTypes.int32_t in parameter.DataFormat):
                modulo = len(datastring) % 8
                for i in range(0, (len(datastring)-modulo), 8):
                # for i in range(0, len(datastring), 8):
                    splited_data.append(str(struct.unpack('<i', bytes.fromhex(datastring[i:i+8]))[0]))
            elif(self.dataTypes.float in parameter.DataFormat):
                modulo = len(datastring) % 8
                for i in range(0, (len(datastring)-modulo), 8):
                # for i in range(0, len(datastring), 8):
                    splited_data.append(str(struct.unpack('<f', bytes.fromhex(datastring[i:i+8]))[0]))
            elif(self.dataTypes.double in parameter.DataFormat):
                modulo = len(datastring) % 16
                for i in range(0, (len(datastring)-modulo), 16):
                    splited_data.append(str(struct.unpack('<d', bytes.fromhex(datastring[i:i+16]))[0]))
            elif(self.dataTypes.long in parameter.DataFormat):
                #TODO Long conversion correct?
                for i in range(0, len(datastring), 16):
                    splited_data.append(str(int(datastring[i:i+16], 16)))
            else:
                #not defined type ERROR
                splited_data.append(datastring)
        self.old_processedData = splited_data
        self.saveData(splited_data, parameter)

    def saveData(self, data, parameter):
        """saveData Speichert die Übergebenen Daten anhand der Parameterbezeichnung

        Args:
            data (List): Liste mit verarbeiteten Daten
            parameter (List): Liste mit den zu den Daten gehörigen Parametern
        """
        self.createTextFile(parameter)
        if(len(data) == 1):
            self.writeTextRow(data[0])
        else:
            self.writeTextRows(data)

    def getProcessedData(self):
        """getProcessedData Gibt die fertig verarbeiteten Daten zurück bis v1.4.. noch nicht benutzt

        Returns:
            List: Liste mit verarbeiteten Daten
        """
        return self.old_processedData

    def createTextFile(self, parameter):
        """createTextFile Erstellt eine Textdatei anhand des übergebenen Parameters

        Args:
            parameter (Parameter): Parameter
        """
        self.filePath = self.filePath + '/' + str(parameter.GUI_id) + '.txt'
        if(not os.path.exists(self.filePath) or not self.filePath):
            self.filePath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
            self.filePath = self.filePath + '/' + str(parameter.GUI_id) + '.txt'
            with open(self.filePath, 'a', encoding='UTF8', newline='') as f:
                f.write(parameter.CSV_text + '\n')

    def writeTextRow(self, data):
        """writeTextRow Schreibt eine Zeile in die zuvor erstellte Textdatei

        Args:
            data (String): Datenstring
        """
        with open(self.filePath, 'a', encoding='UTF8') as f:
            f.write(data + '\n')

    def writeTextRows(self, data):
        """writeTextRows Schreibt mehrere Zeilen in die zuvor erstellte Textdatei

        Args:
            data (List): Liste mit Datenstring (pro Listeneintrag eine Zeile)
        """
        with open(self.filePath, 'a', encoding='UTF8') as f:
            for i in range(0, len(data)):
                f.write(data[i] + '\n')
              # f.writelines(data)
