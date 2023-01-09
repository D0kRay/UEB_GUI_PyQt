#define StatusFlags_OS 0
#define ID_OS 1
#define Count_OS 2
#define MaxPackage_OS 3
#define Data_OS 4

class DT_algorithmus():

    PACKET_SIZE = 128 #128/2 = 64 bytes Packet size
    TRANSMISSION_COMPLETE = "80fe"
    message_packages = list
    transmitted_data_info = list
    data_list = list

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
                if(self.TRANSMISSION_COMPLETE in searchString):
                    messageEndPoint = i
            if(not messageEndPoint == 0):
                for i in range((len(splitedTransLength)-1), messageEndPoint, -1):
                    splitedTransLength.pop(i)
            self.message_packages = splitedTransLength.copy()
            self.data_list.append(splitedTransLength.)

            
        

    def getTransmittedDataInfo(self):
        pass

    def getDataPacket(self, dataname):
        pass

