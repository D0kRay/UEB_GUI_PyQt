import sys
import serial
import serial.tools.list_ports
import threading
import time

from serial import Serial
from scpi_commands import scpi_commands


class Communication:

    ser = Serial
    t = threading
    scpi_commands = scpi_commands
    
    def __init__(self):
        self.thread_run = False
        self.ser = Serial(None, 115200, timeout = 0)
        self.scpi_commands = scpi_commands()
        
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
            self.ser = Serial(port, 115200, timeout = 0)
            connected = True
        else:
            self.ser.close()

        return connected
        # self.writeCommmand(scpi_commands.UEBREADY)
        # self.readSerialRead()

    def readSerialRead(self):
        self.t = threading.Thread(target=self.threadreadSerial, daemon=True)
        self.thread_run = True
        self.t.start()

    def threadreadSerial(self):
        while self.thread_run:
            data = self.ser.readline()
            data_decoded = data.decode('ascii')
            print(data_decoded)

            
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


   
    




