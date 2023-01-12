#define StatusFlags_OS 0
#define ID_OS 1
#define Count_OS 2
#define MaxPackage_OS 3
#define Data_OS 4
from data_content import data_content

class DT_algorithmus():

    PACKET_SIZE = 128 #128/2 = 64 bytes Packet size
    TRANSMISSION_COMPLETE = "80"
    ID_STATUS_PACKET_HEX = "00"
    ID_STATUS_PACKET_DEC = 0
    STATUS_PACKET_IDENTIFIER = "StatusPacket"
    STATUSFLAG_BYTE_LIST_NR = 0
    GUIID_BYTE_LIST_NR = 2
    # CONTROLLERID_BYTE_LIST_NR = 4
    COUNT_BYTE_LIST_NR = 4
    MAXPACKAGE_BYTE_LIST_NR = 6
    DATA_BYTE_LIST_NR = 8

    id_datatype_list = list
    sorted_transmission_data = list

    def __init__(self):
        self.id_datatype_list = []
        self.sorted_transmission_data = []

    def processQueue(self, queue):
        if(not queue.empty()):
            singleTransmission = (queue.get()).hex()
            # singleTransmission = queue.get()
            splitedTransLength = [singleTransmission[i:i+self.PACKET_SIZE] for i in range(0, len(singleTransmission), self.PACKET_SIZE)]
            parityCheck = len(singleTransmission) % 2
            if(not parityCheck == 0):
                print("**********Fehler bei der Uebertragung! Modulo 2 Fehler**********")
            messageEndPoint = 0
            for i in range(0, len(splitedTransLength)):
                if(self.TRANSMISSION_COMPLETE in (splitedTransLength[i][:2])):
                    messageEndPoint = i
            if(not messageEndPoint == 0):
                for i in range((len(splitedTransLength)-1), messageEndPoint, -1):
                    splitedTransLength.pop(i)
            for i in range(0, len(splitedTransLength)):
                self.disassembleOnePacket(splitedTransLength[i])

        

            
    def disassembleOnePacket(self, inpacket):
        appended_to_sorted_datalist = False
        if(self.ID_STATUS_PACKET_HEX in inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)]):
            outPacket = ["StatusPacket", inpacket]
            if(len(self.sorted_transmission_data)):
                for i in range(0, len(self.sorted_transmission_data)):
                    if(self.sorted_transmission_data[i][0].GUI_id == int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)], 16)):
                        packet = data_content()
                        packet.GUI_id = int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)
                        packet.StatusPacket = True
                        packet.Data = inpacket
                        self.sorted_transmission_data[i].append(packet)
                        appended_to_sorted_datalist = True

            if(not appended_to_sorted_datalist):
                packet = data_content()
                packet.GUI_id = int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)
                packet.StatusPacket = True
                packet.Data = inpacket
                self.sorted_transmission_data.append([packet])
        else:
            outPacket = ["StatusFlag", inpacket[self.STATUSFLAG_BYTE_LIST_NR:(self.STATUSFLAG_BYTE_LIST_NR+2)], "GUI_ID", inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)], "Count", inpacket[self.COUNT_BYTE_LIST_NR:(self.COUNT_BYTE_LIST_NR+2)], "MaxPackage", inpacket[self.MAXPACKAGE_BYTE_LIST_NR:(self.MAXPACKAGE_BYTE_LIST_NR+2)], "Data", inpacket[self.DATA_BYTE_LIST_NR:]]
            # outPacket = ["StatusFlag", inpacket[:2], "ID", inpacket[2:4], "Count", inpacket[4:6], "MaxPackage", inpacket[6:8], "Data", self.disassembleDataBasedOnDataType(inpacket[8:], inpacket[2:4])]
            if(len(self.sorted_transmission_data)):
                for i in range(0, len(self.sorted_transmission_data)):
                    if(self.sorted_transmission_data[i][0].GUI_id == int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)):
                        packet = data_content()
                        packet.Status_Byte = inpacket[self.STATUSFLAG_BYTE_LIST_NR:(self.STATUSFLAG_BYTE_LIST_NR+2)]
                        packet.GUI_id = int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)
                        packet.Count = int(inpacket[self.COUNT_BYTE_LIST_NR:(self.COUNT_BYTE_LIST_NR+2)],16)
                        packet.MaxPackages = int(inpacket[self.MAXPACKAGE_BYTE_LIST_NR:(self.MAXPACKAGE_BYTE_LIST_NR+2)],16)
                        packet.Data = inpacket[self.DATA_BYTE_LIST_NR:]
                        self.sorted_transmission_data[i].append(packet)
                        appended_to_sorted_datalist = True
                    
            if(not appended_to_sorted_datalist):
                packet = data_content()
                packet.Status_Byte = inpacket[self.STATUSFLAG_BYTE_LIST_NR:(self.STATUSFLAG_BYTE_LIST_NR+2)]
                packet.GUI_id = int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)
                packet.Count = int(inpacket[self.COUNT_BYTE_LIST_NR:(self.COUNT_BYTE_LIST_NR+2)],16)
                packet.MaxPackages = int(inpacket[self.MAXPACKAGE_BYTE_LIST_NR:(self.MAXPACKAGE_BYTE_LIST_NR+2)],16)
                packet.Data = inpacket[self.DATA_BYTE_LIST_NR:]
                self.sorted_transmission_data.append([packet])
        return outPacket

    def disassembleDataBasedOnDataType(self, data, id):
        # TODO Datensätze anhand ihrer Datengröße erstellen und in Data als Liste von einzelnen Daten abspeichern
        pass

    def getTransmittedIDs(self):
        id_list = []
        for i in range(0, len(self.sorted_transmission_data)):
            if(not self.ID_STATUS_PACKET_DEC == (self.sorted_transmission_data[i][0].GUI_id)):
                id_list.append(self.sorted_transmission_data[i][0].GUI_id)
        return id_list

    def getCompleteDataPacket(self, id):
        dataPacket = []
        for i in range(0, len(self.sorted_transmission_data)):
            if((self.sorted_transmission_data[i])[0].GUI_id == id):
                dataPacket = self.sorted_transmission_data[i]
        return dataPacket

        
    def getPendingDataPacket(self, id):
        dataPacket = []
        for i in range(0, len(self.sorted_transmission_data)):
            if((self.sorted_transmission_data[i])[0].GUI_id == id):
                for j in range(0, len(self.sorted_transmission_data[i])):
                    if(not self.sorted_transmission_data[i][j].DataFetched):
                        self.sorted_transmission_data[i][j].DataFetched = True
                        dataPacket.append(self.sorted_transmission_data[i][j])
        return dataPacket
               

    def setDataTypes(self, idDatatypeList):
        self.id_datatype_list = idDatatypeList

    def isTransmissionComplete(self, id):
        transmission_complete = False
        for i in range(0, len(self.sorted_transmission_data)):
            if((self.sorted_transmission_data[i])[0].GUI_id == id and (len(self.sorted_transmission_data[i])-1) == self.sorted_transmission_data[i][0].MaxPackages):
                transmission_complete = True
        return transmission_complete

