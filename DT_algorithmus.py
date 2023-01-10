#define StatusFlags_OS 0
#define ID_OS 1
#define Count_OS 2
#define MaxPackage_OS 3
#define Data_OS 4

class DT_algorithmus():

    PACKET_SIZE = 128 #128/2 = 64 bytes Packet size
    TRANSMISSION_COMPLETE = "80"
    ID_STATUS_PACKET = "00"
    STATUS_PACKET_IDENTIFIER = "StatusPacket"
    message_buffer = list
    transmitted_data_info = list
    data_list = list
    id_datatype_list = list
    sorted_transmission_data = list

    def __init__(self):
        self.data_list = []
        self.message_buffer = []
        self.id_datatype_list = []
        self.sorted_transmission_data = []

    def processQueue(self, queue):
        if(not queue.empty()):
            singleTransmission = (queue.get()).hex()
            splitedTransLength = [singleTransmission[i:i+self.PACKET_SIZE] for i in range(0, len(singleTransmission), self.PACKET_SIZE)]
            parityCheck = len(singleTransmission) % 2
            if(not parityCheck == 0):
                print("**********Fehler bei der Uebertragung! Modulo 2 Fehler**********")
            messageEndPoint = 0
            for i in range(0, len(splitedTransLength)):
                searchString = splitedTransLength[i]
                packetinfo = searchString[:2]
                if(self.TRANSMISSION_COMPLETE in packetinfo):
                    messageEndPoint = i
            if(not messageEndPoint == 0):
                for i in range((len(splitedTransLength)-1), messageEndPoint, -1):
                    splitedTransLength.pop(i)
            for i in range(0, len(splitedTransLength)):
                disassembled = self.disassembleOnePacket(splitedTransLength[i])
                self.data_list.append(disassembled)
                self.message_buffer.append(disassembled)

        

            
    def disassembleOnePacket(self, inpacket):
        if(self.ID_STATUS_PACKET in inpacket[2:4]):
            outPacket = ["StatusPacket", inpacket]
        else:
            outPacket = ["StatusFlag", inpacket[:2], "ID", inpacket[2:4], "Count", inpacket[4:6], "MaxPackage", inpacket[6:8], "Data", inpacket[8:]]
            # outPacket = ["StatusFlag", inpacket[:2], "ID", inpacket[2:4], "Count", inpacket[4:6], "MaxPackage", inpacket[6:8], "Data", self.disassembleDataBasedOnDataType(inpacket[8:], inpacket[2:4])]

        return outPacket

    def disassembleDataBasedOnDataType(self, data, id):
        # TODO Datensätze anhand ihrer Datengröße erstellen und in Data als Liste von einzelnen Daten abspeichern
        pass

    def getTransmittedIDs(self):
        id_list = []
        for i in range (0, len(self.data_list)):
            if(not self.STATUS_PACKET_IDENTIFIER in (self.data_list[i])[0]):
                idAt_i = (self.data_list[i])[3]
                if(not idAt_i in id_list):
                    id_list.append(idAt_i)
        return id_list

    def getDataPacket(self, id):
        dataPacket = []
        buffer_delelte_id_rows = []
        for i in range(0, len(self.message_buffer)):
            packet = self.message_buffer[i]
            if(not self.STATUS_PACKET_IDENTIFIER in packet[0]):
                if(id in packet[3]):
                    dataPacket.append(packet)
                    buffer_delelte_id_rows.append(i)

        if(len(buffer_delelte_id_rows) > 0):
            buffer_delelte_id_rows.reverse()
            while not len(buffer_delelte_id_rows) == 0:
                self.message_buffer.pop(buffer_delelte_id_rows[0])
                buffer_delelte_id_rows.pop(0)

        return dataPacket

    def setDataTypes(self, idDatatypeList):
        self.id_datatype_list = idDatatypeList
