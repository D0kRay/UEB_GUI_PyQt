import csv
import os
import threading
import time

import pyqtgraph as pg
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QFileDialog, QLabel, QMainWindow,
                             QPushButton)
from pyqtgraph import PlotWidget, plot
from qt_material import apply_stylesheet

from communication import Communication
from csv_writer import csv_writer
from DT_algorithmus import DT_algorithmus
from scpi_commands import scpi_commands
from ueb_config import ueb_config
from ui_MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    SAFE_INTERVAL_FILE = 0.2  #seconds

    hour = [1,2,3,4,5,6,7,8,9,10]
    temperature = [30,32,34,32,33,31,29,32,35,45]
    savePath = ""

    communication = Communication
    ueb_config = ueb_config()
    ueb_config_list = list
    scpi_commands = scpi_commands
    dt_algorithmus = DT_algorithmus
    csv_datacolumns = list

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.scpi_commands = scpi_commands()
        self.communication = Communication()
        self.dt_algorithmus = DT_algorithmus()
        self.job = Job(interval=self.SAFE_INTERVAL_FILE, execute=self.getDataFromThread, name="DataSafeThread")
        self.savePath = ""
        self.csv_datacolumns = []
        self.fileheaderCreated = False
        self.plotWidget_UEB_status_lower = pg.PlotWidget()
        self.plotWidget_UEB_status_upper = pg.PlotWidget()
        self.setupUi(self)
        self.RDCRes_comboBox_Resolver.addItems(["10 bit", "12 bit", "14 bit", "16 bit"])
        self.EncoderRes_comboBox_Resolver.addItems(["10 bit", "12 bit", "14 bit", "16 bit"])

        self.saveunder_Button.clicked.connect(self.saveFileDialog)
        self.refreshComPort_Button.clicked.connect(self.refreshComPortComboBox)
        self.exit_Button.clicked.connect(self.exitButtonClicked)
        self.connectComPort_Button.clicked.connect(self.connectButtonClicked)
        self.einstLesen_pushButton_UEB.clicked.connect(self.readUEB_SettingsButtonClicked)
        self.einst_Schreiben_pushButton_UEB.clicked.connect(self.writeUEB_SettingsButtonClicked)
        self.startButton_UEB_status.clicked.connect(self.startMotor)


    def showGUI(self):
        window = self
        window.setWindowIcon(QIcon("UEB_icon.png"))
        window.setWindowTitle("UEB")
        window.plotWidget_UEB_status_upper.plot(self.hour, self.temperature)
        window.show()


    def saveFileDialog(self):
        fileName, _ = QFileDialog.getSaveFileName(self,"Speichern unter:","","All Files (*);;Text Files (*.csv)")
        if fileName:
            self.savePath = fileName
            print(fileName)

        
    def refreshComPortComboBox(self):
        self.comPort_comboBox.clear()
        self.comPort_comboBox.addItems(self.communication.getComPorts())

    def exitButtonClicked(self):
        if("Disconnect" in self.connectComPort_Button.text()):
            self.communication.stopThread()
        if(self.job.is_alive()):
            self.job.stop()
        self.close()
        
    def stopButtonClicked(self):
        print("STOP")

    def connectButtonClicked(self):
        comport = self.comPort_comboBox.currentText()
        if("Connect" in self.connectComPort_Button.text()):
            if(len(comport) != 0):
                if(self.communication.setComPort(comport)):
                    print("Comport SET" + comport)
                    settings = self.communication.readSettings()
                    self.ueb_config_list = self.getUEB_SettingVars(settings)
                    self.setUEB_Config(self.ueb_config_list)
                    self.setUEB_Config_Tab()
                    self.connectComPort_Button.setText("Disconnect")
                else:
                    self.connectComPort_Button.setText("Connect")
        else:
            self.communication.stopThread()
            self.connectComPort_Button.setText("Connect")

    def readUEB_SettingsButtonClicked(self):
        if ("Disconnect" in self.connectComPort_Button.text()):
            self.communication.stopThread()
            settings = self.communication.readSettings()
            self.ueb_config_list = self.getUEB_SettingVars(settings)
            self.setUEB_Config(self.ueb_config_list)
            self.setUEB_Config_Tab()

    def writeUEB_SettingsButtonClicked(self):
        self.communication.stopThread()
        self.sendUEBConfigTab()

    def getUEB_SettingVars(self, settingsstring):
        self.communication.stopThread()
        parameters = settingsstring.split(";")
        for i in range(len(parameters)):
            temp = parameters[i].split("=")
            parameters[i] = temp[1]
        temp = parameters[len(parameters)-1].split("\r")
        parameters[len(parameters)-1] = temp[1]

        return parameters

    def setUEB_Config(self, ueb_config_list):
        self.ueb_config.status = ueb_config_list[0]
        self.ueb_config.v_Reference = ueb_config_list[1]
        self.ueb_config.v_Bridge = ueb_config_list[2]
        self.ueb_config.frequency = ueb_config_list[3]
        self.ueb_config.rotationDirection = ueb_config_list[4]
        self.ueb_config.thridHarmonic = ueb_config_list[5]
        self.ueb_config.enableSoftstarter = ueb_config_list[6]
        self.ueb_config.softstartDuration = ueb_config_list[7]
        self.ueb_config.overCurrentThreshold = ueb_config_list[7]

    def setUEB_Config_Tab(self):
        self.frequenz_SpinBox_UEB.setValue(float(self.ueb_config.frequency))
        self.versorgSp_SpinBox_UEB.setValue(float(self.ueb_config.v_Reference))
        self.ausgangSp_SpinBox_UEB.setValue(float(self.ueb_config.v_Bridge))
        self.softstart_checkBox_UEB.setChecked(bool(int(self.ueb_config.enableSoftstarter)))
        self.softstartD_SpinBox_UEB.setValue(float(self.ueb_config.softstartDuration))
        self.dritteHarm_checkBox_UEB.setChecked(bool(int(self.ueb_config.thridHarmonic)))
        if(bool(int(self.ueb_config.rotationDirection))):
            self.rightturn_radioButton_UEB.setChecked(True)
            self.leftturn_radioButton_UEB.setChecked(False)
        else:
            self.leftturn_radioButton_UEB.setChecked(True)
            self.rightturn_radioButton_UEB.setChecked(False)
        # self.pwmFrq_SpinBox_UEB

    def sendUEBConfigTab(self):
        self.communication.writeCommand(self.scpi_commands.setUEBRotation(self.rightturn_radioButton_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBThridHarmonic(self.dritteHarm_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartEnable(self.softstart_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartDuration(self.softstartD_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVBridge(self.versorgSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVout(self.ausgangSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBFrequency(self.frequenz_SpinBox_UEB.value()))

    def startMotor(self):
        if ("Disconnect" in self.connectComPort_Button.text()):
            self.generateParameterColumns()
            if(self.measureAtStartup_checkBox_UEB_status.isChecked() and not self.savePath):
                self.saveFileDialog()
            if(self.savePath):
                self.createFile()
            self.communication.writeCommand(self.scpi_commands.setDatatransmission())
            self.communication.readSerialRead()
            self.startDataProcessThread()

    def startDataProcessThread(self):
        if(not self.job.is_alive()):
            self.job = Job(interval=self.SAFE_INTERVAL_FILE, execute=self.getDataFromThread, name="DataProcessThread")
            self.job.start()

    def stopMotor(self):
        if ("Disconnect" in self.connectComPort_Button.text()):
            self.communication.writeCommand("DT\r")
            self.communication.readSerialRead()

    def writeFileHeader(self, ids):
        self.fileheaderCreated = True
        header = []
        for i in range(0, len(ids)):
            if(ids[i] in self.parametercolumns):
                header.append(self.parametercolumns[self.parametercolumns.index(ids[i]) + 1])
        self.writeRow(header)

    def generateParameterColumns(self):
        self.parametercolumns = [self.hex0.text(), self.csv0.text(), self.hex1.text(), self.csv1.text(), self.hex2.text(), self.csv2.text(), 
        self.hex3.text(), self.csv3.text(), self.hex4.text(), self.csv4.text(), self.hex5.text(), self.csv5.text(), self.hex6.text(), self.csv6.text(), 
        self.hex7.text(), self.csv7.text(), self.hex8.text(), self.csv8.text(), self.hex9.text(), self.csv9.text(), self.hex10.text(), self.csv10.text()]
        

    def createFile(self):
        if(not os.path.exists(self.savePath)):
            with open(self.savePath, 'x', encoding='UTF8', newline='') as f:
                self.writer = csv.writer(f)
                # self.writer.writerow(header)


    def writeRow(self, data):
        with open(self.savePath, 'a', encoding='UTF8', newline='') as f:
            self.writer = csv.writer(f)
            self.writer.writerow(data)

    def getDataFromThread(self):
        # data_array = self.communication.thread_data_queue
        # laenge = data_array.qsize()
        self.dt_algorithmus.processQueue(self.communication.thread_data_queue)
        transmittedIDs = self.dt_algorithmus.getTransmittedIDs()
        for i in range(0, len(transmittedIDs)):
            self.csv_datacolumns.append(self.dt_algorithmus.getDataPacket(transmittedIDs[i]))

        
        for j in range(0, len(self.csv_datacolumns[0])):
            rowData = []
            for i in range(0, len(self.csv_datacolumns)):
                    rowData.append(((self.csv_datacolumns[i])[j])[9])

            if(self.savePath):
                if(not self.fileheaderCreated):
                    self.writeFileHeader(transmittedIDs)          
                self.writeRow(rowData)

        self.csv_datacolumns.clear()
            
    
class Job(threading.Thread):
    def __init__(self, interval, execute, name, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        self.name = name
        
    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval):
                self.execute(*self.args, **self.kwargs)


