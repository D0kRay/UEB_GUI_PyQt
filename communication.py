import sys
import serial
import serial.tools.list_ports
import threading
import time

from serial import Serial
from scpi_commands import scpi_commands
from threading import Thread
from threading import Event


class Communication:

    ser = Serial
    t = threading
    scpi_commands = scpi_commands
    stop_event = Event
    
    def __init__(self):
        self.thread_run = False
        self.ser = Serial(None, 256000, timeout = 0)
        self.scpi_commands = scpi_commands()
        self.stop_event = Event()
    
        
    def getComPorts(self):
        self.ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(self.ports):
            print("{}: {} [{}]".format(port, desc, hwid))

        portlist = []

        for port in sorted(self.ports):
            portlist.append(port.name)

        return portlist

    def setComPort(self, port):
        connected = False
        if(not self.ser.is_open):
            print("OPEN")
            self.ser = Serial(port, 256000, timeout = 0, parity = serial.PARITY_NONE, rtscts = 1)
            self.ser.set_buffer_size(rx_size=12800, tx_size=12800)
            connected = True
        else:
            self.ser.close()

        return connected
        # self.writeCommmand(scpi_commands.UEBREADY)
        # self.readSerialRead()

    def readSerialRead(self):
        if(not self.thread_run):
            # self.stop_event = Event()
            self.t = threading.Thread(target=self.threadreadSerial, name="SerialThread", args=(self.stop_event,), daemon=True) #TODO doppeltes Komma?
            self.thread_run = True
            self.t.start()
            # self.start = time.time()
            print(time.time())
            

    def threadreadSerial(self, event):
        while not event.is_set():
            if(self.ser.is_open):
                data = self.ser.read(self.ser.in_waiting)
                # data = self.ser.readline()
                # if(not data == b''):
                    # print(data)
                    # print(time.time())
                    # print("Starttime:" + str(self.start))
        print('Thread stopped')

    def stopThread(self):
        self.stop_event.set()
        self.t.join()
                    
    def writeCommand(self, command):
        # command = command + scpi_commands.CARRIAGE_RETURN
        bytestring = command.encode('ascii')
        self.ser.write(bytestring)

    def readSettings(self):
        self.writeCommand(self.scpi_commands.getUEBsettings())
        time.sleep(0.2)
        data = self.ser.readline()
        data_decoded = data.decode('ascii')
        return data_decoded


   
    




