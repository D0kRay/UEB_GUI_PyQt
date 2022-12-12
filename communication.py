import sys
import serial
import serial.tools.list_ports


class Communication:

    serial_handler = serial 
    ports = list

    def __init__(self) -> None:
        pass

        
    def getComPorts(self):
        self.ports = self.serial_handler.tools.list_ports.comports()

        for port, desc, hwid in sorted(self.ports):
            print("{}: {} [{}]".format(port, desc, hwid))

        portlist = []

        for port in sorted(self.ports):
            portlist.append(port.name)

        return portlist




