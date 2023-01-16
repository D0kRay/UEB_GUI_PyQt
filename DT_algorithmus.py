#define StatusFlags_OS 0
#define ID_OS 1
#define Count_OS 2
#define MaxPackage_OS 3
#define Data_OS 4
import time 

from scpi_commands import scpi_commands
from data_content import DataContent
from threading import Event, Thread
from queue import Queue
from communication import Communication

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

    communication = Communication
    scpi_commands = scpi_commands
    dt_thread = Thread
    dt_data_queue = Queue
    id_datatype_list = list
    sorted_transmission_data = list
    stop_event = Event
    thread_run = bool
    unique_id = int


    def __init__(self):
        self.id_datatype_list = []
        self.sorted_transmission_data = []
        self.thread_run = False
        self.stop_event = Event()
        self.dt_thread = Thread()
        self.scpi_commands = scpi_commands()
        self.dt_data_queue = Queue(maxsize=0)
        self.id_list = []
        # self.communication = communication
        self.unique_id = 0
        # self.startDTthread()

    def processQueue(self, queue):
        if(not queue.empty()):
            singleTransmission = (queue.get()).hex()
            # singleTransmission = queue.get()
            splitedTransLength = [singleTransmission[i:i+self.PACKET_SIZE] for i in range(0, len(singleTransmission), self.PACKET_SIZE)]
            parityCheck = len(singleTransmission) % 2
            if(not parityCheck == 0):
                print("**********Fehler bei der Uebertragung! Modulo 2 Fehler**********")
            # messageEndPoint = 0
            # for i in range(0, len(splitedTransLength)):
                # if(self.TRANSMISSION_COMPLETE in (splitedTransLength[i][:2])):
                #     messageEndPoint = i
            # if(not messageEndPoint == 0):
            #     for i in range((len(splitedTransLength)-1), messageEndPoint, -1):
            #         splitedTransLength.pop(i)
            for i in range(0, len(splitedTransLength)):
                packet = self.disassembleOnePacket(splitedTransLength[i])
                self.id_list.append([packet.GUI_id, packet.Count])


        

            
    def disassembleOnePacket(self, inpacket):
        appended_to_sorted_datalist = False
        unique_id_transmission = -1
        if(self.ID_STATUS_PACKET_HEX in inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)]):
            # outPacket = ["StatusPacket", inpacket]
            if(len(self.sorted_transmission_data)):
                for i in range(0, len(self.sorted_transmission_data)):
                    if(self.sorted_transmission_data[i][0].GUI_id == int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)], 16)):
                        if(self.sorted_transmission_data[i][0].Status_Byte == -10):
                            unique_id_transmission = self.sorted_transmission_data[i][0].UniqueID
                            self.sorted_transmission_data[i].pop(0)
                        else:
                            unique_id_transmission = self.sorted_transmission_data[i][0].UniqueID

                        packet = DataContent()
                        packet.GUI_id = int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)
                        packet.StatusPacket = True
                        packet.UniqueID = unique_id_transmission
                        packet.Data = inpacket
                        self.sorted_transmission_data[i].append(packet)
                        appended_to_sorted_datalist = True

            if(not appended_to_sorted_datalist):
                packet = DataContent()
                packet.GUI_id = int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)
                packet.StatusPacket = True
                packet.Data = inpacket
                self.sorted_transmission_data.append([packet])
        else:
            # outPacket = ["StatusFlag", inpacket[self.STATUSFLAG_BYTE_LIST_NR:(self.STATUSFLAG_BYTE_LIST_NR+2)], "GUI_ID", inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)], "Count", inpacket[self.COUNT_BYTE_LIST_NR:(self.COUNT_BYTE_LIST_NR+2)], "MaxPackage", inpacket[self.MAXPACKAGE_BYTE_LIST_NR:(self.MAXPACKAGE_BYTE_LIST_NR+2)], "Data", inpacket[self.DATA_BYTE_LIST_NR:]]
            # outPacket = ["StatusFlag", inpacket[:2], "ID", inpacket[2:4], "Count", inpacket[4:6], "MaxPackage", inpacket[6:8], "Data", self.disassembleDataBasedOnDataType(inpacket[8:], inpacket[2:4])]
            if(len(self.sorted_transmission_data)):
                for i in range(0, len(self.sorted_transmission_data)):
                    if(self.sorted_transmission_data[i][0].GUI_id == int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)):
                        if(self.sorted_transmission_data[i][0].Status_Byte == -10):
                            unique_id_transmission = self.sorted_transmission_data[i][0].UniqueID
                            self.sorted_transmission_data[i].pop(0)
                        else:
                            unique_id_transmission = self.sorted_transmission_data[i][0].UniqueID

                        packet = DataContent()
                        packet.Status_Byte = inpacket[self.STATUSFLAG_BYTE_LIST_NR:(self.STATUSFLAG_BYTE_LIST_NR+2)]
                        packet.GUI_id = int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)
                        packet.Count = int(inpacket[self.COUNT_BYTE_LIST_NR:(self.COUNT_BYTE_LIST_NR+2)],16)
                        packet.MaxPackages = int(inpacket[self.MAXPACKAGE_BYTE_LIST_NR:(self.MAXPACKAGE_BYTE_LIST_NR+2)],16)
                        packet.UniqueID = unique_id_transmission
                        packet.Data = inpacket[self.DATA_BYTE_LIST_NR:]
                        self.sorted_transmission_data[i].append(packet)
                        appended_to_sorted_datalist = True
                    
            if(not appended_to_sorted_datalist):
                packet = DataContent()
                packet.Status_Byte = inpacket[self.STATUSFLAG_BYTE_LIST_NR:(self.STATUSFLAG_BYTE_LIST_NR+2)]
                packet.GUI_id = int(inpacket[self.GUIID_BYTE_LIST_NR:(self.GUIID_BYTE_LIST_NR+2)],16)
                packet.Count = int(inpacket[self.COUNT_BYTE_LIST_NR:(self.COUNT_BYTE_LIST_NR+2)],16)
                packet.MaxPackages = int(inpacket[self.MAXPACKAGE_BYTE_LIST_NR:(self.MAXPACKAGE_BYTE_LIST_NR+2)],16)
                packet.Data = inpacket[self.DATA_BYTE_LIST_NR:]
                self.sorted_transmission_data.append([packet])

        #TODO Pakete für die Konfiguration noch disassemblen 
        #Eigene ID für StatusPakete
        return packet

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

    # Gui methode
    def setTransmissionPackets(self, id_list):
        unique_id_list = []
        for i in range(0, len(id_list)):
            data_obj = DataContent()
            data_obj.GUI_id(id_list[i])
            data_obj.UniqueID = self.unique_id
            data_obj.Status_Byte = -10
            unique_id_list.append(self.unique_id)
            self.sorted_transmission_data.append(data_obj)
            self.unique_id = self.unique_id + 1
        return unique_id_list

    # Gui methode
    def getPacket(self, unique_id):
        dataPacket = []
        datastring = ''
        for i in range(0, len(self.sorted_transmission_data)):
            if((self.sorted_transmission_data[i])[0].UniqueID == unique_id):
                for j in range(0, len(self.sorted_transmission_data[i])):
                    datastring = datastring + self.sorted_transmission_data[i][j].Data
                dataPacket = [self.sorted_transmission_data[i].UniqueID, datastring]
        return dataPacket
               

    def setDataTypes(self, idDatatypeList):
        self.id_datatype_list = idDatatypeList

    def isTransmissionComplete(self, id):
        transmission_complete = False
        for i in range(0, len(self.sorted_transmission_data)):
            if((self.sorted_transmission_data[i])[0].GUI_id == id and (len(self.sorted_transmission_data[i])-1) == self.sorted_transmission_data[i][0].MaxPackages):
                transmission_complete = True
        return transmission_complete

    def sendTransmissionComplete(self, id):
        self.communication.writeCommand(self.scpi_commands.setDatatransmissionComplete(hex(id)))

    def startDTthread(self):
        if(not self.thread_run):
            self.stop_event.clear()
            # self.communication.readSerialRead()
            self.dt_thread = Thread(target=self.DT_thread, name="DT_Thread", args=(self.stop_event, self.dt_data_queue), daemon=True) 
            self.thread_run = True
            time.sleep(0.5)
            self.dt_thread.start()

    def DT_thread(self, stop_event, queue):
        while not stop_event.is_set():
            print(".")
            # self.processQueue(self.communication.thread_data_queue)
            # transmittedIDs = self.getTransmittedIDs()
            # for i in range(0, len(transmittedIDs)):
            #     # data = DT_algoObj.getPendingDataPacket(transmittedIDs[i])
            #     # self.csv_datacolumns.append(data)
            #     # transmissionComplete = self.dt_algorithmus.isTransmissionComplete(transmittedIDs[i])
            #     if(self.isTransmissionComplete(transmittedIDs[i])):
            #         self.sendTransmissionComplete(self, hex(transmittedIDs[i]))
            #         queue.put(self.dt_algorithmus.getCompleteDataPacket(transmittedIDs[i]))








