import platform
import sys
import threading
import time
from queue import Queue
from threading import Event, Thread

import serial
import serial.tools.list_ports
from serial import Serial

from scpi_commands import scpi_commands


class Communication:

    ser = Serial
    t = threading
    scpi_commands = scpi_commands
    stop_event = Event
    thread_data_queue = Queue
    
    def __init__(self):
        self.thread_run = False
        self.ser = Serial(None, 256000, timeout = 0)
        self.scpi_commands = scpi_commands()
        self.stop_event = Event()     
        self.thread_data_queue = Queue(maxsize=0)
    
        
    def getComPorts(self):
        """getComPorts Gibt die aktuellen COM Ports des Rechners zurück

        Returns:
            List: Liste mit COM Ports
        """
        self.ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(self.ports):
            print("{}: {} [{}]".format(port, desc, hwid))

        portlist = []

        for port in sorted(self.ports):
            portlist.append(port.name)

        return self.ports
        # return portlist

    def setComPort(self, port):
        """setComPort Öffnet den übergebenen COM Port des Rechners

        Args:
            port (String): COM Port 

        Returns:
            Boolean: True bei erfolgreichem Öffnen
        """
        connected = False
        if(not self.ser.is_open):
            operating_system = ''
            operating_system = platform.system()
            try:
                if(operating_system == 'Darwin'):
                    port = '/dev/' + port
                self.ser = Serial(port, 256000, timeout = 0, parity = serial.PARITY_NONE, rtscts = 1)
                if(not operating_system == 'Darwin'):
                    self.ser.set_buffer_size(rx_size=128000, tx_size=128000)
                connected = True
                print("COM Port " + port + " geoeffnet")
            except:
                print("COM Port kann nicht geoeffnet werden.")
        else:
            self.ser.close()

        return connected

    def closeComPort(self):
        """closeComPort Schließt den aktuell geöffneten COM Port
        """
        if(self.ser.is_open):
            self.ser.close()


    def readSerialRead(self):
        """readSerialRead Startet den COM Port Lese Thread
        """
        if(not self.thread_run):
            self.stop_event.clear()
            self.t = threading.Thread(target=self.threadreadSerial, name="SerialThread", args=(self.ser, self.stop_event, self.thread_data_queue), daemon=True) 
            self.thread_run = True
            self.t.start()
            # print(time.time())
            

    def threadreadSerial(self, serialobj, eventobj, queue):
        """threadreadSerial Threadmethode der seriellen Kommunikation (leseseitig)

        Args:
            serialobj (Serial): Serielle Schnittstelle
            eventobj (Event): Eventobjekt zum stoppen des Threads
            queue (Queue): Queue in die die Daten der Seriellen Schnittstelle gespeichert werden
        """
        while not eventobj.is_set():
            try:
                if(serialobj.is_open and serialobj.in_waiting > 0):
                    buffer = (serialobj.read(serialobj.in_waiting))
                    serialobj.flushInput()
                    queue.put(buffer)
            except:
                print("Uebertragungsfehler **SerialThread**")
                eventobj.set()
        print('Serialthread stopped')

    def stopThread(self):
        """stopThread Stoppt den seriellen Lesethread
        """
        if(self.thread_run):
            self.stop_event.set()
            self.t.join()
            self.thread_run = False
                    
    def writeCommand(self, command):
        """writeCommand Schickt das übergebene Kommando an den Controller

        Args:
            command (String): Kommando
        """
        try:
            bytestring = command.encode('ascii')
            self.ser.flushInput()
            self.ser.write(bytestring)
        except:
            print("Eingabe konnte nicht dekodiert werden!")

    def readSettings(self):
        """readSettings Liest die Einstellungen des Controllers aus 

        Returns:
            String: Erhaltener Datenstring (empty String bei fehlerhafter Übertragung)
        """
        self.writeCommand(self.scpi_commands.getUEBsettings())
        time.sleep(0.2)
        data = self.ser.readline()
        try:
            data_decoded = data.decode('ascii')
        except:
            print("Uebertragung der Settings fehlerhaft. Versuchen Sie es erneut.")
            # data_decoded = "STAT= 1;VCC= 0;VOUT= 0;FREQ= 0;ROT= 0;TRDHARM= 0;SOFTSTART= 0;DUR= 0;CURR= 0\r\x00"
        return data_decoded

    


   
    




