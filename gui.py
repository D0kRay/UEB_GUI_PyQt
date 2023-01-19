import csv
import os
import time
import json
import threading

import pyqtgraph as pg
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QObject, QThread, QThreadPool, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QSizePolicy, QFileDialog, QLabel, QHBoxLayout,
                             QVBoxLayout, QWidget)
from pyqtgraph import PlotWidget, plot
# from qt_material import apply_stylesheet

from communication import Communication
from DT_algorithmus import DT_algorithmus
from scpi_commands import scpi_commands
from ueb_config import ueb_config
from ui_MainWindow import Ui_MainWindow
from ui_parameter_dialog import Ui_TransmissionParameterDialog
from parameter import Parameter
from resolver_config import ResolverConfig
from gui_data import GuiData
from transmission_dialog import TransmissionDialog
from data_analyser import DataAnalyser

# class RefreshThread(QThread):


    
#     data_string = QtCore.pyqtSignal()
#     data_list = QtCore.pyqtSignal()


#     def __init__(self, dt_algorithmus, parent=None):
#         QThread.__init__(self, parent)
#         # QtCore.QThread.__init__(self)
#         self.dt_algorithmus = dt_algorithmus
#         self.datastring = ''

#     def run(self):

#         self.checkDTAlgorithmusQueue()
#         # time.sleep(0.1)
#         ##andere Funktionen
        

#     def checkDTAlgorithmusQueue(self):
#             while not self.dt_algorithmus.dt_data_queue.empty():
#                 queue_element = self.dt_algorithmus.dt_data_queue.get()
#                 # self.processQueueElement(queue_element)
#                 self.data_string.emit(str(queue_element))

##TODO Datenrückgabe an GUI


        # self.dt_algorithmus.processQueue(self.communication.thread_data_queue)
        # transmittedIDs = self.dt_algorithmus.getTransmittedIDs()
        
        # for i in range(0, len(transmittedIDs)):
        #     data = self.dt_algorithmus.getPendingDataPacket(transmittedIDs[i])
        #     # self.csv_datacolumns.append(data)
        #     # transmissionComplete = self.dt_algorithmus.isTransmissionComplete(transmittedIDs[i])
        #     if((not len(data)) == 0 and self.dt_algorithmus.isTransmissionComplete(transmittedIDs[i])):
        #         self.communication.writeCommand(self.scpi_commands.setDatatransmissionComplete(hex(transmittedIDs[i])))
        #         filename = self.createTextFile(self.getCSVTextFromID(transmittedIDs[i]))
        #         complete_data = self.dt_algorithmus.getCompleteDataPacket(transmittedIDs[i])
        #         datastring_terminal = ''
        #         for j in range(0, len(complete_data)):
        #             datastring_terminal = datastring_terminal + complete_data[i].Data
        #             # label = QLabel(text=complete_data[i].Data)
        #             # self.TerminalScroll_UEBTransmissionScrollAreaLayout.addWidget(label)
        #             # complete_data[i] = str(complete_data[i].Data)
        #         # self.terminal_textlabel.setText(self.terminal_textlabel.text() + datastring_terminal)
        #         # self.writeHeader(transmittedIDs[i])
        #         self.writeTextRow(str(transmittedIDs[i]), filename)
        #         self.writeTextRow(datastring_terminal, filename)
        #         print('ID: ' + str(transmittedIDs[i]) + ' saved')

    # def processQueueElement(self, queueItem):
    #         self.


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    UEB_GUI_VERSION = 1.2

    savePath = ""
    REFRESH_INTERVAL = 0.1

    communication = Communication
    ueb_config = ueb_config
    resolver_config = ResolverConfig
    ueb_config_list = list
    scpi_commands = scpi_commands
    dt_algorithmus = DT_algorithmus
    csv_datacolumns = list
    plot_data_upper = list #Datastructure: [0] plot on/off [1] color [2] lineobj [3] x list [4] y list [5] data
    plot_data_lower = list #Datastructure: [0] plot on/off [1] color [2] lineobj [3] x list [4] y list [5] data
    separated_id_list = list
    parameter_list = list
    data_list = list
    transmission_dialog = TransmissionDialog
    # refreshThread = RefreshThread
    # thread = QThread


    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.scpi_commands = scpi_commands()
        self.communication = Communication()
        self.dt_algorithmus = DT_algorithmus()
        self.data_analyser = DataAnalyser()
        self.job = Job(interval=self.REFRESH_INTERVAL, execute=self.processData, name="DataSafeThread")
        # self.refresh_thread = Thread()
        self.savePath = ''
        self.parameterFilepath = ''
        self.terminalString = ''
        self.csv_datacolumns = []
        self.plot_data_upper = []
        self.plot_data_lower = []
        self.separated_id_list = []
        self.parameter_list = []
        self.predefined_parameter_list = []
        self.data_list = []
        self.ueb_config = ueb_config()
        self.resolver_config = ResolverConfig()
        # self.thread = QThread()
        # self.refreshThread = RefreshThread(self.dt_algorithmus)
        # self.refreshThread.started.connect(self.refreshThread.run)
        # self.refreshThread.moveToThread(self.thread)
        # self.thread.started.connect(self.refreshThread.run)
        self.fileheaderCreated = False
        self.thread_run = False
        self.plotWidget_UEB_status_lower = pg.PlotWidget()
        self.plotWidget_UEB_status_upper = pg.PlotWidget()
        self.UEBTransmissionScrollAreaLayout = QVBoxLayout()
        self.TerminalScroll_verticalLayout = QVBoxLayout()
        self.terminalTimer = QTimer()
        self.terminalTimer.timeout.connect(self.refreshTerminal)

        self.setupUi(self)
        self.tabWidget.setCurrentIndex(1)   #always start at ueb settings
        self.refreshComPortComboBox()

        self.terminal_widget = QWidget()
        self.terminal_widget.setLayout(self.TerminalScroll_verticalLayout)
        # self.terminal_scrollArea.setWidgetResizable(True)

        self.terminal_scrollArea.setWidget(self.terminal_widget)

        
        # self.startRefreshThread()
        # self.dialog = QDialog(self)
        # Ui_NewParameterDialog.setupUi(self.dialog)
        self.RDCRes_comboBox_Resolver.addItems(["10 bit", "12 bit", "14 bit", "16 bit"])
        self.EncoderRes_comboBox_Resolver.addItems(["10 bit", "12 bit", "14 bit", "16 bit"])
        self.plotWidget_UEB_status_lower.setBackground('w')
        self.plotWidget_UEB_status_upper.setBackground('w')

        self.saveunder_Button.clicked.connect(self.savePathDialog)
        self.refreshComPort_Button.clicked.connect(self.refreshComPortComboBox)
        self.exit_Button.clicked.connect(self.exitButtonClicked)
        self.stop_Button.clicked.connect(self.stopMotor)
        self.connectComPort_Button.clicked.connect(self.connectButtonClicked)
        self.einstLesen_pushButton_UEB.clicked.connect(self.readUEB_SettingsButtonClicked)
        self.einst_Schreiben_pushButton_UEB.clicked.connect(self.writeUEB_SettingsButtonClicked)
        self.startButton_UEB_status.clicked.connect(self.startMotor)
        self.saveTransmissionParameter_pushButton.clicked.connect(self.safeParameterToJSON)
        self.loadTransmissionParameter_pushButton.clicked.connect(self.loadParameterFromJSON)
        self.openParameterDialog_pushButton.clicked.connect(self.showTransmissinoParameterDialog)
        self.saveUEBSettings_pushButton.clicked.connect(self.safeUEBToJSON)
        self.loadUEBSettings_pushButton.clicked.connect(self.loadUEBFromJSON)
        self.startMeasureUEBSettings_pushButton.clicked.connect(self.startMeasure)
        self.terminal_userline.returnPressed.connect(self.transmitTerminalUserInput)

        ##Release V1.1
        ##Felder in UEB Einstellungen werden teils der Bedienbarkeit wegen ausgeblendet.
        if(self.UEB_GUI_VERSION == 1.1):
            self.tabWidget.setTabVisible(0, False)
            self.tabWidget.setTabVisible(2, False)
            # self.tabWidget.setTabVisible(3, False)
            self.UEB_SettingsTransmission_scrollArea.setVisible(False)
            self.loadTransmissionParameter_pushButton.setVisible(False)
            self.openParameterDialog_pushButton.setVisible(False)
            self.saveTransmissionParameter_pushButton.setVisible(False)
            self.UEB_Transmissionsettings_label.setVisible(False)
            try:
                self.parameterFilepath = os.getcwd() + '/predefined_parameter.json'
                self.loadParameterFromJSON()
            except:
                print("predefined_parameter.json nicht gefunden!")
                print("Nur ID 224 kann übertragen werden!")
                parameter = Parameter()
                parameter.GUI_id = 224
                parameter.CSV_text = "224"
                self.parameter_list.append(parameter)
        ##
        if(self.UEB_GUI_VERSION == 1.2):
            try:
                self.parameterFilepath = os.getcwd() + '/predefined_parameter.json'
                self.loadParameterFromJSON()
            except:
                print("Vorkonfiguration nicht moeglich, da *predefined_parameter.json* nicht auslesbar")





    def showGUI(self):
        window = self
        window.setWindowIcon(QIcon("UEB_icon.png"))
        window.setWindowTitle("UEB")
        window.show()

    # def startRefreshThread(self):
    #     self.refreshThread.data_string.connect(self.refreshTerminal)
    #     self.refreshThread.start()        
    #     # if(not self.thread_run):
    #     #     self.stop_event.clear()
    #     #     self.data_processed.connect(self.processDataForGUI)
    #     #     self.refresh_thread = Thread(target=self.processData, name="Refresh_Thread", args=(self, self.stop_event), daemon=True) 
    #     #     self.thread_run = True
    #     #     self.refresh_thread.start()

    def processDataForGUI(self):
        print('d')

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

    def refreshTerminal(self):
        if(len(self.terminalString) != 0):
            sizePolicy = QSizePolicy()
            sizePolicy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
            terminalLabel = QLabel()
            terminalLabel.setText(self.terminalString)
            terminalLabel.setSizePolicy(sizePolicy)
            self.TerminalScroll_verticalLayout.addWidget(terminalLabel)
            self.terminalString = ''

    def transmitTerminalUserInput(self):
        if ("Disconnect" in self.connectComPort_Button.text()):
            userString = ''
            userString = self.terminal_userline.text() + '\r'
            if(len(userString) < 1023):
                self.terminal_userline.clear()
                self.communication.writeCommand(userString)
                self.terminalString = "GUI: " + userString
                self.refreshTerminal()


    def savePathDialog(self):
        Path = QFileDialog.getExistingDirectory(self,"Speichern unter:","")
        if Path:
            self.savePath = Path
            print(Path)

    def saveFileDialog(self):
        filepath = QFileDialog.getSaveFileName(self,"Speichern unter:", "", "Text Files (*.txt)")
        if filepath:
            self.savePath = filepath
            print(filepath)

        
    def refreshComPortComboBox(self):   
        self.comPort_comboBox.clear()
        self.comPort_comboBox.addItems(self.communication.getComPorts())

    def exitButtonClicked(self):
        if("Disconnect" in self.connectComPort_Button.text()):
            self.communication.stopThread()
            self.communication.closeComPort()
            self.terminalTimer.stop()
        if(self.job.is_alive()):
            self.job.stop()
        self.close()
        
    def stopButtonClicked(self):
        print("STOP")

    def connectButtonClicked(self):
        comport = self.comPort_comboBox.currentText()
        if("Connect" in self.connectComPort_Button.text()):
            if(len(comport) != 0):
                self.terminalTimer.start(300)
                if(self.communication.setComPort(comport)):
                    print("Comport SET " + comport)
                    settings = self.communication.readSettings()
                    if(settings):
                        self.ueb_config_list = self.getUEB_SettingVars(settings)
                        self.setUEB_Config(self.ueb_config_list)
                        self.setUEB_Config_Tab()
                        self.communication.readSerialRead()
                        self.startDataProcessThread()
                        self.connectComPort_Button.setText("Disconnect")
                    else:
                        print("Falscher COM Port oder Fehlerhafte Uebertragung.")
                        self.communication.closeComPort()
                else:
                    self.connectComPort_Button.setText("Connect")
        else:
            self.communication.stopThread()
            self.terminalTimer.stop()
            self.communication.closeComPort()
            self.terminalTimer.stop()
            if(self.job.is_alive()):
                self.job.stop()
            print("Disconnected")
            self.connectComPort_Button.setText("Connect")

    def readUEB_SettingsButtonClicked(self):
        if ("Disconnect" in self.connectComPort_Button.text()):
            # self.communication.stopThread()
            self.communication.writeCommand(self.scpi_commands.getUEBsettings())
            # settings = self.communication.readSettings()
            # self.ueb_config_list = self.getUEB_SettingVars(settings)
            # self.setUEB_Config(self.ueb_config_list)
            # self.setUEB_Config_Tab()

    def writeUEB_SettingsButtonClicked(self):
        # self.communication.stopThread()
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
#TODO RESolver Kommandos und view
    def setResolver_Config(self, ueb_config_list):
        self.resolver_config.status = ueb_config_list[0]
        self.resolver_config.v_Reference = ueb_config_list[1]
        self.resolver_config.v_Bridge = ueb_config_list[2]
        self.resolver_config.frequency = ueb_config_list[3]
        self.resolver_config.rotationDirection = ueb_config_list[4]
        self.resolver_config.thridHarmonic = ueb_config_list[5]
        self.resolver_config.enableSoftstarter = ueb_config_list[6]
        self.resolver_config.softstartDuration = ueb_config_list[7]
        self.resolver_config.overCurrentThreshold = ueb_config_list[7]

    def setResolver_Config_Tab(self):
        self.frequenz_SpinBox_UEB.setValue(float(self.resolver_config.frequency))
        self.versorgSp_SpinBox_UEB.setValue(float(self.resolver_config.v_Reference))
        self.ausgangSp_SpinBox_UEB.setValue(float(self.resolver_config.v_Bridge))
        self.softstart_checkBox_UEB.setChecked(bool(int(self.resolver_config.enableSoftstarter)))
        self.softstartD_SpinBox_UEB.setValue(float(self.resolver_config.softstartDuration))
        self.dritteHarm_checkBox_UEB.setChecked(bool(int(self.resolver_config.thridHarmonic)))
        if(bool(int(self.resolver_config.rotationDirection))):
            self.rightturn_radioButton_UEB.setChecked(True)
            self.leftturn_radioButton_UEB.setChecked(False)
        else:
            self.leftturn_radioButton_UEB.setChecked(True)
            self.rightturn_radioButton_UEB.setChecked(False)

    def sendResolverConfigTab(self):
        self.communication.writeCommand(self.scpi_commands.setUEBRotation(self.rightturn_radioButton_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBThridHarmonic(self.dritteHarm_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartEnable(self.softstart_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartDuration(self.softstartD_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVBridge(self.versorgSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVout(self.ausgangSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBFrequency(self.frequenz_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBsettings(True))

    def startMotor(self):
        if ("Disconnect" in self.connectComPort_Button.text() and not (len(self.parameter_list) == 0)):
            if(self.measureAtStartup_checkBox_UEB_status.isChecked() and not self.savePath):
                self.savePathDialog()          
            self.communication.readSerialRead()
            self.startDataProcessThread()
            self.startButton_UEB_status.setText("Motor läuft")
            self.startMeasureUEBSettings_pushButton.setText("Messung läuft")


            if (not self.job.is_alive()):
                timer = QTimer()
                timer.timeout.connect(self.sendParameter)
                timer.setSingleShot(True)
                timer.start(2000)
            else:
                self.sendParameter()
            
            # time.sleep(3)
            # for i in range(0, len(self.parameter_list)):
            #     if(not int(self.parameter_list[i].GUI_id) == 0):
            #         self.communication.writeCommand(self.scpi_commands.setDatatransmissionInit(self.parameter_list[i].GUI_id))   

    def startMeasure(self):
        if ("Disconnect" in self.connectComPort_Button.text() and not (len(self.parameter_list) == 0)):
            if(self.measureAtStartup_checkBox_UEB_status.isChecked() and not self.savePath):
                self.savePathDialog()          
            self.communication.readSerialRead()
            self.startDataProcessThread()
            self.startButton_UEB_status.setText("Motor läuft")
            self.startMeasureUEBSettings_pushButton.setText("Messung läuft")
            # closeWaitMessageBox = False
            # waitdialog = QMessageBox(self)
            # waitdialog.setWindowTitle("Messung starten?")
            # waitdialog.setText("Messung starten?")
            # waitdialog.exec()
            if (not self.job.is_alive()):
                timer = QTimer()
                timer.timeout.connect(self.sendParameter)
                timer.setSingleShot(True)
                timer.start(2000)
            else:
                self.sendParameter()
            
            # # time.sleep(3)
            # for i in range(0, len(self.parameter_list)):
            #     if(not int(self.parameter_list[i].GUI_id) == 0):
            #         self.communication.writeCommand(self.scpi_commands.setDatatransmissionInit(self.parameter_list[i].GUI_id))   
            # # waitdialog.close()
            # print("Max Threads verfügbar: " + str(QThreadPool.globalInstance().maxThreadCount()))
            
    def startDataProcessThread(self):
        if(not self.job.is_alive()):
            self.job = Job(interval=self.REFRESH_INTERVAL, execute=self.processData, name="DataProcessThread")
            self.job.start()

    def sendParameter(self):
        for i in range(0, len(self.parameter_list)):
                if(not int(self.parameter_list[i].GUI_id) == 0):                   
                    self.communication.writeCommand(self.scpi_commands.setDatatransmissionInit(self.parameter_list[i].GUI_id))   
                    self.terminalString = self.terminalString + self.scpi_commands.setDatatransmissionInit(self.parameter_list[i].GUI_id) + '\r'
            # waitdialog.close()
        print("Max Threads verfügbar: " + str(QThreadPool.globalInstance().maxThreadCount()))
        

    def stopMotor(self):
        if ("Disconnect" in self.connectComPort_Button.text()):
            print("Motor stop")
            self.terminalTimer.stop()
            self.startButton_UEB_status.setText("Motor starten")
            self.startMeasureUEBSettings_pushButton.setText("Messung starten")
            # self.communication.writeCommand("DT:CONFIG\r")
            # self.communication.readSerialRead()

    def showTransmissinoParameterDialog(self):
        if(self.parameterFilepath):
            self.loadParameterFromJSON()
        dialog = self.transmission_dialog(self.parameter_list)
        dialog.setWindowTitle("Übertragungseinstellungen")
        dialog.setWindowIcon(QIcon("UEB_icon.png"))
        if dialog.exec():
            self.parameter_list = dialog.getParameterList()
            self.setUEBTransmissionSettingsWindow()
        else:
            print('Dialog closed')

    # def getCSVTextFromID(self, id):
    #     csv_text = 'n.v.'
    #     for i in range(0, len(self.parameter_list)):
    #         if(str(id) in self.parameter_list[i].GUI_id):
    #             csv_text = self.parameter_list[i].GUI_id
    #     return csv_text

    def setUEBTransmissionSettingsWindow(self):
        self.clearLayout(self.UEBTransmissionScrollAreaLayout)
        for i in range(0, len(self.parameter_list)):
            parameterObj = self.parameter_list[i]
            idLabel = QLabel()
            csvLabel = QLabel()
            datatypeLabel = QLabel()
            delimiterLabel = QLabel()
            sizePolicy = QSizePolicy()
            sizePolicy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
            idLabel.setText(parameterObj.GUI_id)
            idLabel.setMinimumSize(40,30)
            idLabel.setSizePolicy(sizePolicy)
            csvLabel.setText(parameterObj.CSV_text)
            datatypeLabel.setText(parameterObj.DataFormat)
            delimiterLabel.setText(parameterObj.delimiter)
            rowlayout = QHBoxLayout()
            rowlayout.addWidget(idLabel)
            rowlayout.addWidget(csvLabel)
            rowlayout.addWidget(datatypeLabel)
            rowlayout.addWidget(delimiterLabel)
            self.UEBTransmissionScrollAreaLayout.addLayout(rowlayout)
            self.UEB_SettingsTransmission_scrollArea.setLayout(self.UEBTransmissionScrollAreaLayout)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                childlayout = layout.takeAt(0)
                if childlayout.widget() is not None:
                    childlayout.widget().deleteLater()
                elif childlayout.layout() is not None:
                    self.clearLayout(childlayout.layout())


    def safeParameterToJSON(self):
        jsonString = json.dumps([ob.__dict__ for ob in self.parameter_list])
        fileName, _ = QFileDialog.getSaveFileName(self,"Speichern unter:","","Text Files (*.json)")
        jsonFile = open(fileName, 'w')
        jsonFile.write(jsonString)
        jsonFile.close()

    def loadParameterFromJSON(self):
        if(not self.parameterFilepath):
            self.parameterFilepath, _ = QFileDialog.getOpenFileName(self,"Speichern unter:","","Text Files (*.json)")
        if(self.parameterFilepath):
            jsonFile = open(self.parameterFilepath, 'r')
            jsonString = jsonFile.read()
            filecontent = json.loads(jsonString)
            paramlist = []
            for i in range(0, len(filecontent)):
                parameter = Parameter()
                parameter.CSV_text = filecontent[i]['CSV_text']
                parameter.DataFormat = filecontent[i]['DataFormat']
                parameter.DT_id = filecontent[i]['DT_id']
                parameter.GUI_id = filecontent[i]['GUI_id']
                parameter.row = filecontent[i]['row']
                paramlist.append(parameter)
            self.parameter_list = paramlist
            jsonFile.close()

            # for i in range(224, 250):
            #     parameter = Parameter()
            #     parameter.CSV_text = str(i)
            #     parameter.DataFormat = ''
            #     parameter.DT_id = ''
            #     parameter.GUI_id = str(i)
            #     parameter.row = ''
            #     self.parameter_list.append(parameter)
    
            self.setUEBTransmissionSettingsWindow()

    def safeUEBToJSON(self):
        fileName, _ = QFileDialog.getSaveFileName(self,"Speichern unter:","","Text Files (*.json)")
        if(fileName):
            jsonString = json.dumps(vars(self.ueb_config))
            jsonFile = open(fileName, 'w')
            jsonFile.write(jsonString)
            jsonFile.close()

    def loadUEBFromJSON(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"Speichern unter:","","Text Files (*.json)")
        if(fileName):
            jsonFile = open(fileName, 'r')
            jsonString = jsonFile.read()
            filecontent = json.loads(jsonString)
            self.ueb_config = ueb_config()
            self.ueb_config.frequency = filecontent['frequency']
            self.ueb_config.v_Bridge = filecontent['v_Bridge']
            self.ueb_config.v_Reference = filecontent['v_Reference']
            self.ueb_config.softstartDuration = filecontent['softstartDuration']
            self.ueb_config.overCurrentThreshold = filecontent['overCurrentThreshold']
            self.ueb_config.pwmFrequency = filecontent['pwmFrequency']
            self.ueb_config.rotationDirection = filecontent['rotationDirection']
            self.ueb_config.thridHarmonic = filecontent['thridHarmonic']
            self.ueb_config.enableSoftstarter = filecontent['enableSoftstarter']
            self.setUEB_Config_Tab()
            jsonFile.close()

    # def createFile(self, filename):
    #     if(not os.path.exists(self.savePath) or not self.savePath):
    #         self.savePath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    #     filename = filename + '.csv'
    #     with open((self.savePath + '/' + filename), 'w', encoding='UTF8', newline='') as f:
    #         self.writer = csv.writer(f)
    #         # self.writer.writerow(filename)
    #     return filename

    # def createTextFile(self, filename):
    #     if(not os.path.exists(self.savePath) or not self.savePath):
    #         self.savePath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    #     filename = filename + '.txt'
    #     with open((self.savePath + '/' + filename), 'w', encoding='UTF8', newline='') as f:
    #         f.write('')
    #         # self.writer.writerow(filename)
    #     return filename

    # def writeTextRow(self, data, filename):
    #     # filename = filename + '.csv'
    #     filename = filename + '.txt'
    #     with open((self.savePath + '/' + filename), 'a', encoding='UTF8') as f:
    #         f.write(data + '\n')

    # def writeHeader(self, ids):
    #     self.fileheaderCreated = True
    #     self.generateParameterList()
    #     header = []
    #     for i in range(0, len(ids)):
    #         for j in range(0, len(self.parameter_list)):
    #             if ids[i] in self.parameter_list[j].row:
    #                 header.append(self.parameter_list[j].CSV_text)
    #     self.writeRow(header)


    # def writeRow(self, data, filename):
    #     with open((self.savePath + '/' + filename), 'a', encoding='UTF8', newline='') as f:
    #         self.writer = csv.writer(f)
    #         self.writer.writerow(data)

    # def writeCompleteCSV(self, data, filename):
    #     with open((self.savePath + '/' + filename), 'a', encoding='UTF8', newline='') as f:
    #         self.writer = csv.writer(f)
    #         self.writer.writerows(data)

    def getParameterOfData(self, data):
        parameter = Parameter()
        for i in range(0, len(self.parameter_list)):
            if(str(data[0].GUI_id) in self.parameter_list[i].GUI_id):
                parameter = self.parameter_list[i]
                break
        return parameter


    def processData(self):
        self.dt_algorithmus.processQueue(self.communication.thread_data_queue)
        transmittedIDs = self.dt_algorithmus.getTransmittedIDs()
        
        for i in range(0, len(transmittedIDs)):
            data = self.dt_algorithmus.getPendingDataPacket(transmittedIDs[i])
            if((not len(data)) == 0 and self.dt_algorithmus.isTransmissionComplete(transmittedIDs[i])):
                self.communication.writeCommand(self.scpi_commands.setDatatransmissionComplete(transmittedIDs[i]))
                complete_data = self.dt_algorithmus.getCompleteDataPacket(transmittedIDs[i])
                datastring = ''
                terminalstring = "Controller: ID " + str(transmittedIDs[i]) + '\n'
                data_parameter = Parameter
                for j in range(0, len(complete_data)):
                    datastring = datastring + complete_data[j].Data
                    terminalstring = terminalstring + complete_data[j].Data + '\n'
                self.terminalString = self.terminalString + terminalstring
                if(complete_data[0].GUI_id == 255):
                    self.ueb_config_list = self.getUEB_SettingVars(complete_data[0].Data)
                    self.setUEB_Config(self.ueb_config_list)
                    self.setUEB_Config_Tab()
                else:
                    data_parameter = self.getParameterOfData(complete_data)
                    self.data_analyser.processData(complete_data, data_parameter, self.savePath)
                print("ID " + str(transmittedIDs[i]) + " erfolgreich uebertragen!")

            
            
        
    
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
                print("Dataprocessthread stopped")
    def run(self):
            while not self.stopped.wait(self.interval):
                self.execute(*self.args, **self.kwargs)
