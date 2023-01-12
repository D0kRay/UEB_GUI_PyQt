import csv
import os
import threading
import time
import json

import pyqtgraph as pg
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QFileDialog, QLabel, QMainWindow,
                             QPushButton, QSpinBox, QLineEdit)
from pyqtgraph import PlotWidget, plot
from qt_material import apply_stylesheet

from communication import Communication
from DT_algorithmus import DT_algorithmus
from scpi_commands import scpi_commands
from ueb_config import ueb_config
from ui_MainWindow import Ui_MainWindow
from parameter import parameter_transmission


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    SAFE_INTERVAL_FILE = 0.1  #seconds

    hour = [1,2,3,4,5,6,7,8,9,10]
    temperature = [30,32,34,32,33,31,29,32,35,45]
    savePath = ""

    communication = Communication
    ueb_config = ueb_config()
    ueb_config_list = list
    scpi_commands = scpi_commands
    dt_algorithmus = DT_algorithmus
    csv_datacolumns = list
    plot_data_upper = list #Datastructure: [0] plot on/off [1] color [2] lineobj [3] x list [4] y list [5] data
    plot_data_lower = list #Datastructure: [0] plot on/off [1] color [2] lineobj [3] x list [4] y list [5] data
    separated_id_list = list
    parameter_list = list

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.scpi_commands = scpi_commands()
        self.communication = Communication()
        self.dt_algorithmus = DT_algorithmus()
        self.job = Job(interval=self.SAFE_INTERVAL_FILE, execute=self.getDataFromThread, name="DataSafeThread")
        self.savePath = ""
        self.csv_datacolumns = []
        self.plot_data_upper = []
        self.plot_data_lower = []
        self.separated_id_list = []
        self.parameter_list = []
        self.fileheaderCreated = False
        self.plotWidget_UEB_status_lower = pg.PlotWidget()
        self.plotWidget_UEB_status_upper = pg.PlotWidget()
        self.setupUi(self)
        self.RDCRes_comboBox_Resolver.addItems(["10 bit", "12 bit", "14 bit", "16 bit"])
        self.EncoderRes_comboBox_Resolver.addItems(["10 bit", "12 bit", "14 bit", "16 bit"])
        self.plotWidget_UEB_status_lower.setBackground('w')
        self.plotWidget_UEB_status_upper.setBackground('w')

        self.saveunder_Button.clicked.connect(self.saveFileDialog)
        self.refreshComPort_Button.clicked.connect(self.refreshComPortComboBox)
        self.exit_Button.clicked.connect(self.exitButtonClicked)
        self.connectComPort_Button.clicked.connect(self.connectButtonClicked)
        self.einstLesen_pushButton_UEB.clicked.connect(self.readUEB_SettingsButtonClicked)
        self.einst_Schreiben_pushButton_UEB.clicked.connect(self.writeUEB_SettingsButtonClicked)
        self.startButton_UEB_status.clicked.connect(self.startMotor)
        self.saveTransmissionparameter_pushButton.clicked.connect(self.safeParameterToJSON)
        self.loadTransmissionparameter_pushButton.clicked.connect(self.loadParameterFromJSON)


    def showGUI(self):
        window = self
        window.setWindowIcon(QIcon("UEB_icon.png"))
        window.setWindowTitle("UEB")
        window.show()

    def plotOnUEBStatusPlots(self):
        # TODO Plots aus liste laden und aktualisieren
        if(len(self.plot_data_upper)):
            for i in range(0, len(self.plot_data_upper)):
                if((self.plot_data_upper[i])[0]):
                    if(len(self.plot_data_upper[i]) < 4):
                        x = (self.plot_data_upper[i])[3]
                        y = (self.plot_data_upper[i])[4]
                        line_obj = self.plotWidget_UEB_status_upper.plot(x, y)
                        self.plot_data_upper.insert(2, line_obj)
                    else:
                        (self.plot_data_upper[i])[3] = ((self.plot_data_upper[i])[3])[1:]
                        (self.plot_data_upper[i])[4] = ((self.plot_data_upper[i])[4])[1:]
                        self.plot_data_upper[2].setData(self.hour, self.temperature)
        elif(len(self.plot_data_lower)):
            for i in range(0, len(self.plot_data_lower)):
                if((self.plot_data_lower[i])[0]):
                    if(len(self.plot_data_lower[i]) < 4):
                        x = (self.plot_data_lower[i])[3]
                        y = (self.plot_data_lower[i])[4]
                        line_obj = self.plotWidget_UEB_status_lower.plot(x, y)
                        self.plot_data_lower.insert(2, line_obj)
                    else:
                        (self.plot_data_lower[i])[3] = ((self.plot_data_lower[i])[3])[1:]
                        (self.plot_data_lower[i])[4] = ((self.plot_data_lower[i])[4])[1:]
                        self.plot_data_lower[2].setData(self.hour, self.temperature)

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
                    print("Comport SET " + comport)
                    settings = self.communication.readSettings()
                    if(settings):
                        self.ueb_config_list = self.getUEB_SettingVars(settings)
                        self.setUEB_Config(self.ueb_config_list)
                        self.setUEB_Config_Tab()
                        self.connectComPort_Button.setText("Disconnect")
                    else:
                        print("Falscher COM Port oder Fehlerhafte Uebertragung.")
                        self.communication.closeComPort()
                else:
                    self.connectComPort_Button.setText("Connect")
        else:
            self.communication.stopThread()
            if(self.job.is_alive()):
                self.job.stop()
            print("Disconnected")
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
        # self.communication.stopThread()
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

    def sendUEBConfigTab(self):
        self.communication.writeCommand(self.scpi_commands.setUEBRotation(self.rightturn_radioButton_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBThridHarmonic(self.dritteHarm_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartEnable(self.softstart_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartDuration(self.softstartD_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVBridge(self.versorgSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVout(self.ausgangSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBFrequency(self.frequenz_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBsettings(True))

    def startMotor(self):
        if ("Disconnect" in self.connectComPort_Button.text()):
            self.generateParameterList()
            if(self.measureAtStartup_checkBox_UEB_status.isChecked() and not self.savePath):
                self.saveFileDialog()
            if(self.savePath):
                self.createFile()
            id = []
            self.dt_algorithmus = DT_algorithmus()
            self.communication.readSerialRead()
            self.startDataProcessThread()
            for i in range(0, len(self.parameter_list)):
                if(not int(self.parameter_list[i].GUI_id) == 0):
                    self.communication.writeCommand(self.scpi_commands.setDatatransmissionInit(self.parameter_list[i].GUI_id))   
            # self.communication.writeCommand(self.scpi_commands.setDatatransmission())
            

    def startDataProcessThread(self):
        if(not self.job.is_alive()):
            self.job = Job(interval=self.SAFE_INTERVAL_FILE, execute=self.getDataFromThread, name="DataProcessThread")
            self.job.start()

    def stopMotor(self):
        if ("Disconnect" in self.connectComPort_Button.text()):
            self.communication.writeCommand("DT:CONFIG\r")
            self.communication.readSerialRead()

    def writeFileHeader(self, ids):
        self.fileheaderCreated = True
        self.generateParameterList(self)
        header = []
        for i in range(0, len(ids)):
            for j in range(0, len(self.parameter_list)):
                if ids[i] in self.parameter_list[j].row:
                    header.append(self.parameter_list[j].CSV_text)
        # for i in range(0, len(ids)):
        #     if(ids[i] in self.parameterlist):
        #         header.append(self.parameterlist[self.parameterlist.index(ids[i]) + 1])
        self.writeRow(header)

    def generateParameterList(self):
        for i in range(0, self.scrollArea_gridLayout_Transmission.count()):
            item = self.scrollArea_gridLayout_Transmission.itemAt(i).widget()
            if isinstance(item, QSpinBox):
                row = 0
                row = ''.join(filter(str.isdigit, item.objectName()))
                if(len(self.parameter_list)):
                    for j in range(0, len(self.parameter_list)):
                        if row in self.parameter_list[j].row:
                            self.parameter_list[j].GUI_id = item.text()
                            break
                        elif(j == (len(self.parameter_list)-1)):
                            parameter = parameter_transmission()
                            parameter.GUI_id = item.text()
                            parameter.row = row
                            self.parameter_list.append(parameter)
                else:
                    parameter = parameter_transmission()
                    parameter.GUI_id = item.text()
                    parameter.row = row
                    self.parameter_list.append(parameter)
            elif(isinstance(item, QLineEdit)):
                if(item.objectName()[:3] == "csv"):
                    row = 0
                    row = ''.join(filter(str.isdigit, item.objectName()))
                    if(len(self.parameter_list)):
                        for j in range(0, len(self.parameter_list)):
                            if row in self.parameter_list[j].row:
                                self.parameter_list[j].CSV_text = item.text()
                                break
                            elif(j == (len(self.parameter_list)-1)):
                                parameter = parameter_transmission()
                                parameter.CSV_text = item.text()
                                parameter.row = row
                                self.parameter_list.append(parameter)
                    else:
                        parameter = parameter_transmission()
                        parameter.CSV_text = item.text()
                        parameter.row = row
                        self.parameter_list.append(parameter)
                elif(item.objectName()[:10] == "dataformat"):
                    row = 0
                    row = ''.join(filter(str.isdigit, item.objectName()))
                    if(len(self.parameter_list)):
                        for j in range(0, len(self.parameter_list)):
                            if row in self.parameter_list[j].row:
                                self.parameter_list[j].DataFormat = item.text()
                                break
                            elif(j == (len(self.parameter_list)-1)):
                                parameter = parameter_transmission()
                                parameter.DataFormat = item.text()
                                parameter.row = row
                                self.parameter_list.append(parameter)
                    else:
                        parameter = parameter_transmission()
                        parameter.DataFormat = item.text()
                        parameter.row = row
                        self.parameter_list.append(parameter)


        # self.parameterlist = []
        # # widgets auf seite Parameter
        # self.parameterlist = [self.id0.text(), self.csv0.text(), self.id1.text(), self.csv1.text(), self.id2.text(), self.csv2.text(), 
        # self.id3.text(), self.csv3.text(), self.id4.text(), self.csv4.text(), self.id5.text(), self.csv5.text(), self.id6.text(), self.csv6.text(), 
        # self.id7.text(), self.csv7.text(), self.id8.text(), self.csv8.text(), self.id9.text(), self.csv9.text(), self.id10.text(), self.csv10.text()]

    def setParameterColumns(self, parametercolumns):

        for i in range(0, self.scrollArea_gridLayout_Transmission.count()):
            item = self.scrollArea_gridLayout_Transmission.itemAt(i).widget()
            if isinstance(item, QSpinBox):
                row = 0
                row = ''.join(filter(str.isdigit, item.objectName()))
                if(len(parametercolumns)):
                    for j in range(0, len(parametercolumns)):
                        if row in parametercolumns[j].row:
                            item.setValue(int(parametercolumns[j].GUI_id))
                            break
            elif(isinstance(item, QLineEdit)):
                if(item.objectName()[:3] == "csv"):
                    row = 0
                    row = ''.join(filter(str.isdigit, item.objectName()))
                    if(len(parametercolumns)):
                        for j in range(0, len(parametercolumns)):
                            if row in parametercolumns[j].row:
                                item.setText(parametercolumns[j].CSV_text)
                                break
                elif(item.objectName()[:10] == "dataformat"):
                    row = 0
                    row = ''.join(filter(str.isdigit, item.objectName()))
                    if(len(parametercolumns)):
                        for j in range(0, len(parametercolumns)):
                            if row in parametercolumns[j].row:
                                item.setText(parametercolumns[j].DataFormat)
                                break

        # self.id0.setText(parametercolumns[0])
        # self.csv0.setText(parametercolumns[1])
        # self.id1.setText(parametercolumns[2])
        # self.csv1.setText(parametercolumns[3])
        # self.id2.setText(parametercolumns[4])
        # self.csv2.setText(parametercolumns[5]) 
        # self.id3.setText(parametercolumns[6])
        # self.csv3.setText(parametercolumns[7])
        # self.id4.setText(parametercolumns[8])
        # self.csv4.setText(parametercolumns[9])
        # self.id5.setText(parametercolumns[10])
        # self.csv5.setText(parametercolumns[11])
        # self.id6.setText(parametercolumns[12])
        # self.csv6.setText(parametercolumns[13]) 
        # self.id7.setText(parametercolumns[14])
        # self.csv7.setText(parametercolumns[15])
        # self.id8.setText(parametercolumns[16])
        # self.csv8.setText(parametercolumns[17])
        # self.id9.setText(parametercolumns[18])
        # self.csv9.setText(parametercolumns[19])
        # self.id10.setText(parametercolumns[20])
        # self.csv10.setText(parametercolumns[21])


    def safeParameterToJSON(self):
        self.generateParameterList()
        jsonString = json.dumps([ob.__dict__ for ob in self.parameter_list])
        jsonFile = open("parameter.json", 'w')
        jsonFile.write(jsonString)
        jsonFile.close()

    def loadParameterFromJSON(self):
        jsonFile = open("parameter.json", 'r')
        jsonString = jsonFile.read()
        filecontent = json.loads(jsonString)
        paramlist = []
        for i in range(0, len(filecontent)):
            parameter = parameter_transmission()
            parameter.CSV_text = filecontent[i]['CSV_text']
            parameter.DataFormat = filecontent[i]['DataFormat']
            parameter.DT_id = filecontent[i]['DT_id']
            parameter.GUI_id = filecontent[i]['GUI_id']
            parameter.row = filecontent[i]['row']
            paramlist.append(parameter)
        self.setParameterColumns(paramlist)
        self.generateParameterList()
        jsonFile.close()

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
            data = self.dt_algorithmus.getPendingDataPacket(transmittedIDs[i])
            # self.csv_datacolumns.append(data)
            # transmissionComplete = self.dt_algorithmus.isTransmissionComplete(transmittedIDs[i])
            if((not len(data)) == 0 and self.dt_algorithmus.isTransmissionComplete(transmittedIDs[i])):
                self.communication.writeCommand(self.scpi_commands.setDatatransmissionComplete(hex(transmittedIDs[i])))
            # if(i >= len(self.separated_id_list)):
                # self.separated_id_list.append(data)
            # else:
            #     self.separated_id_list[i].extend(data)
        # biggestColumn = 0
        # for i in range(0, len(self.csv_datacolumns)):
        #     if(len(self.csv_datacolumns[i]) > biggestColumn):
        #         biggestColumn = len(self.csv_datacolumns[i])
        # for j in range(0, biggestColumn):
        #     rowData = []
        #     for i in range(0, len(self.csv_datacolumns)):
        #         if(len(self.csv_datacolumns[i]) > j):
        #             rowData.append(bytearray.fromhex(((self.csv_datacolumns[i])[j])[9]).decode(errors='ignore'))
        #         else:
        #             rowData.append("")
        #     if(self.savePath):
        #         if(not self.fileheaderCreated):
        #             self.writeFileHeader(transmittedIDs)          
        #         self.writeRow(rowData)
        
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


