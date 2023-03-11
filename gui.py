import csv
import json
import os
import threading
import time

import pyqtgraph as pg
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QObject, QThread, QThreadPool, QTimer
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QSizePolicy,
                             QVBoxLayout, QWidget, QMessageBox)
from pyqtgraph import PlotWidget, plot

from communication import Communication
from data_analyser import DataAnalyser
from DT_algorithmus import DT_algorithmus
from gui_data import GuiData
from parameter import Parameter
from resolver_config import ResolverConfig
from scpi_commands import scpi_commands
from transmission_dialog import TransmissionDialog
from ueb_config import ueb_config
from ui_MainWindow import Ui_MainWindow
from ui_parameter_dialog import Ui_TransmissionParameterDialog
from help_dialog import HelpDialog

# from qt_material import apply_stylesheet



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    UEB_GUI_VERSION = 1.2

    savePath = ""
    REFRESH_INTERVAL = 0.1
    STM32_USB_VID_PID = '1155:22336'
    UEB_INIT = 0
    UEB_RUN_THREEPHASE = 1
    UEB_RUN_DC = 2
    UEB_RUN_CAL_ADC = 3
    UEB_RUN_CONTROL = 4
    UEB_STOP = 5
    UEB_INIT_FINISH = 6

    GUI_DC = "DC Modus"
    GUI_CAL_ADC = "Kalibration ADC"
    GUI_CONTROL = "Regelungsmodus"
    GUI_THREEPHASE = "Dreiphasenmodus"

#define UEB_INIT 0
#define UEB_RUN_THREEPHASE 1
#define UEB_RUN_DC 2
#define UEB_RUN_CAL_ADC 3
#define UEB_RUN_CONTROL 4
#define UEB_STOP 5
#define UEB_INIT_FINISH 6

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
    help_dialog = HelpDialog

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.scpi_commands = scpi_commands()
        self.communication = Communication()
        self.dt_algorithmus = DT_algorithmus()
        self.data_analyser = DataAnalyser()
        self.job = Job(interval=self.REFRESH_INTERVAL, execute=self.processData, name="DataSafeThread")
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
        self.portlist = []
        self.ueb_config = ueb_config()
        self.resolver_config = ResolverConfig()
        self.fileheaderCreated = False
        self.thread_run = False
        self.measure_run = True
        self.measure_started = False
        self.plotWidget_UEB_status_lower = pg.PlotWidget()
        self.plotWidget_UEB_status_upper = pg.PlotWidget()
        self.UEBTransmissionScrollAreaLayout = QVBoxLayout()
        self.TerminalScroll_verticalLayout = QVBoxLayout()
        self.terminalTimer = QTimer()
        self.terminalTimer.timeout.connect(self.refreshTerminal)

        self.setupUi(self)
        self.tabWidget.setCurrentIndex(1)   #always start at ueb settings
        self.refreshComPortComboBox()
        self.setWindowIcon(QIcon("UEB_icon.png"))

        self.terminal_widget = QWidget()
        self.terminal_widget.setLayout(self.TerminalScroll_verticalLayout)

        self.terminal_scrollArea.setWidget(self.terminal_widget)
        self.terminal_userline.setPlaceholderText("Hier Controllerkommando eingeben")
        self.connection_Indicator_Lamp.setStyleSheet("background-color : red")

        self.operation_Mode_comboBox.addItems([self.GUI_DC, self.GUI_THREEPHASE, self.GUI_CONTROL, self.GUI_CAL_ADC])
        self.operation_Mode_comboBox.setCurrentIndex(0)
        self.ueb_config.operationMode = self.operation_Mode_comboBox.currentText()
        self.RDCRes_comboBox_Resolver.addItems(["10 bit", "12 bit", "14 bit", "16 bit"])
        self.EncoderRes_comboBox_Resolver.addItems(["10 bit", "12 bit", "14 bit", "16 bit"])
        self.plotWidget_UEB_status_lower.setBackground('w')
        self.plotWidget_UEB_status_upper.setBackground('w')

        self.saveunder_Button.clicked.connect(self.savePathDialog)
        self.refreshComPort_Button.clicked.connect(self.refreshComPortComboBox)
        self.exit_Button.clicked.connect(self.exitButtonClicked)
        self.stop_Button.clicked.connect(self.stopMotor)
        self.stopButton_UEB_status.clicked.connect(self.stopMotor)
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
        self.help_pushButton.clicked.connect(self.helpMe)
        self.operation_Mode_comboBox.currentTextChanged.connect(self.setUEB_Config_from_UserInput)

        ##Release V1.1
        ##Felder in UEB Einstellungen werden teils der Bedienbarkeit wegen ausgeblendet.
        if(self.UEB_GUI_VERSION == 1.1):
            self.tabWidget.setTabVisible(0, False)
            self.tabWidget.setTabVisible(2, False)
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
        self.parameterFilepath = ''

    def showGUI(self):
        """showGUI Darstellen der GUI
        """
        window = self
        window.setWindowIcon(QIcon("UEB_icon.png"))
        window.setWindowTitle("UEB")
        window.show()

    def helpMe(self):
        dialog = self.help_dialog()
        dialog.setWindowTitle("Hilfe!")
        dialog.setWindowIcon(QIcon("UEB_icon.png"))
        dialog.exec()

    def closeEvent(self, event):
        if("Trennen" in self.connectComPort_Button.text()):
            self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_STOP))
            self.communication.stopThread()
            self.communication.closeComPort()
            self.terminalTimer.stop()
        if(self.job.is_alive()):
            self.job.stop()
        event.accept()


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
        """refreshTerminal Aktualisiert das Terminalfenster anhand des self.Terminalstring
        """
        if(len(self.terminalString) != 0):
            sizePolicy = QSizePolicy()
            sizePolicy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
            terminalLabel = QLabel()
            terminalLabel.setText(self.terminalString)
            terminalLabel.setSizePolicy(sizePolicy)
            self.TerminalScroll_verticalLayout.addWidget(terminalLabel)
            self.terminalString = ''
        if((not self.measure_run) and self.measure_started):
            self.startMeasureUEBSettings_pushButton.setText("Messung starten")
            self.gui_info_dialog_Label.setText("Messung fertig")
            self.measure_run = False
            self.measure_started = False

    
    def transmitTerminalUserInput(self):
        """transmitTerminalUserInput Übertragen der Nutzereingabe auf der Terminalseite
        """
        if ("Trennen" in self.connectComPort_Button.text()):
            userString = ''
            userString = self.terminal_userline.text() + '\r'
            if(len(userString) < 1023):
                self.terminal_userline.clear()
                self.communication.writeCommand(userString)
                self.terminalString = "GUI: " + userString
                self.refreshTerminal()

    def savePathDialog(self):
        """savePathDialog Dialogfenster für die Auswahl des Speicherordners anzeigen
        """
        Path = QFileDialog.getExistingDirectory(self,"Speichern unter:","")
        if Path:
            self.savePath = Path
            print(Path)

    def saveFileDialog(self):
        """saveFileDialog Dialogfenster für die Auswahl der Datei, in welche Daten geschrieben werden sollen
        """
        filepath = QFileDialog.getSaveFileName(self,"Speichern unter:", "", "Text Files (*.txt)")
        if filepath:
            self.savePath = filepath
            print(filepath)
        
    def refreshComPortComboBox(self):
        """refreshComPortComboBox Befüllen der COM Port ComboBox
        """
        self.comPort_comboBox.clear()
        self.portlist = self.communication.getComPorts()
        for i in range(0, len(self.portlist)):
            self.comPort_comboBox.addItem(self.portlist[i].name)

    def exitButtonClicked(self):
        """exitButtonClicked Schließfunktion bei Klick auf den Schließen Button. Es werden alle Threads beendet und die GUI geschlossen
        """
        if("Trennen" in self.connectComPort_Button.text()):
            self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_STOP))
            self.communication.stopThread()
            self.communication.closeComPort()
            self.terminalTimer.stop()
        if(self.job.is_alive()):
            self.job.stop()
        self.close()
        
    def stopButtonClicked(self):
        """stopButtonClicked Stoppt den Motor mit dem UEB_STOP Kommando
        """
        self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_STOP))
        print("STOP")

    def connectButtonClicked(self):
        """connectButtonClicked Versucht eine Verbindung mit der UEB aufzubauen und überprüft ob es sich um den richtigen USB Port handelt
           Es werden bei erfolgreicher Verbindung die Einstellungsparameter der UEB geladen und UEB Einstellungen übernommen
        """
        comport = self.comPort_comboBox.currentText()
        usb_VID_PID = ''
        for i in range(0, len(self.portlist)):
            if(comport in self.portlist[i].name):
                if(self.portlist[i].vid and self.portlist[i].pid):
                    usb_VID_PID = str(self.portlist[i].vid) + ':' + str(self.portlist[i].pid)
        if("Verbinden" in self.connectComPort_Button.text() and (self.STM32_USB_VID_PID in usb_VID_PID)):
            if(len(comport) != 0):
                self.terminalTimer.start(300)
                if(self.communication.setComPort(comport)):
                    print("Comport SET " + comport)
                    settings = self.communication.readSettings()
                    if(len(settings) != 0):
                        self.ueb_config_list = self.getUEB_SettingVars(settings)
                        self.setUEB_Config(self.ueb_config_list)
                        self.setUEB_Config_Tab()
                        self.communication.readSerialRead()
                        self.startDataProcessThread()
                        self.connectComPort_Button.setText("Trennen")
                        self.connection_Indicator_Lamp.setStyleSheet("background-color : green")
                        self.gui_info_dialog_Label.setText("Verbindung aufgebaut")
                    else:
                        print("Falscher COM Port oder Fehlerhafte Uebertragung.")
                        self.communication.closeComPort()
                        self.connection_Indicator_Lamp.setStyleSheet("background-color : red")
                        self.gui_info_dialog_Label.setText("Falscher COM Port oder keine Verbindung")
                else:
                    self.communication.closeComPort()
                    self.connectComPort_Button.setText("Verbinden")
                    self.connection_Indicator_Lamp.setStyleSheet("background-color : red")
                    self.gui_info_dialog_Label.setText("Falscher COM Port oder keine Verbindung")
        else:
            self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_STOP))
            self.communication.stopThread()
            self.terminalTimer.stop()
            self.communication.closeComPort()
            self.terminalTimer.stop()
            if(self.job.is_alive()):
                self.job.stop()
            print("Disconnected")
            self.connectComPort_Button.setText("Verbinden")
            self.connection_Indicator_Lamp.setStyleSheet("background-color : red")
            self.gui_info_dialog_Label.setText("Falscher COM Port oder keine Verbindung")   

    def readUEB_SettingsButtonClicked(self):
        """readUEB_SettingsButtonClicked Die Parameter der UEBs lesen
        """
        if ("Trennen" in self.connectComPort_Button.text()):
            self.communication.writeCommand(self.scpi_commands.getUEBsettings())
            self.gui_info_dialog_Label.setText("Einstellungen von Controller gelesen")

    def writeUEB_SettingsButtonClicked(self):
        """writeUEB_SettingsButtonClicked Die eingestellten Parameter auf die UEB schreiben
        """
        if ("Trennen" in self.connectComPort_Button.text()):
            self.sendUEBConfigTab()
            self.gui_info_dialog_Label.setText("Einstellungen an Controller gesendet")
    
    def setUEB_Config_from_UserInput(self):
        self.ueb_config.operationMode = self.operation_Mode_comboBox.currentText()
        self.ueb_config.frequency = self.frequenz_SpinBox_UEB.value()
        self.ueb_config.v_Reference = self.versorgSp_SpinBox_UEB.value()
        self.ueb_config.v_Bridge = self.ausgangSp_SpinBox_UEB.value()
        self.ueb_config.enableSoftstarter = int(self.softstart_checkBox_UEB.isChecked())
        self.ueb_config.softstartDuration = self.softstartD_SpinBox_UEB.value()
        self.ueb_config.thridHarmonic = int(self.dritteHarm_checkBox_UEB.isChecked())
        self.ueb_config.rotationDirection = int(self.rightturn_radioButton_UEB.isChecked())

    def getUEB_SettingVars(self, settingsstring):
        """getUEB_SettingVars Aufsplitten der übertragenen Parameter in verarbeitbare Datensätze

        Args:
            settingsstring (String): String aus der Kommunikationsschicht

        Returns:
            List: Liste mit den Einstellungen des Controllers
        """
        parameters = settingsstring.split(";")
        for i in range(len(parameters)):
            temp = parameters[i].split("=")
            parameters[i] = temp[1]
        temp = parameters[len(parameters)-1].split("\r")
        parameters[len(parameters)-1] = temp[1]
        return parameters

    def setUEB_Config(self, ueb_config_list):
        """setUEB_Config Beschreiben des ueb_config Objekts mit den übergebenen Werten 

        Args:
            ueb_config_list (List): Liste mit Werten
        """
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
        """setUEB_Config_Tab Übernehmen der Controllerparameter in die GUI Oberfläche
        """
        self.frequenz_SpinBox_UEB.setValue(float(self.ueb_config.frequency))
        self.versorgSp_SpinBox_UEB.setValue(float(self.ueb_config.v_Reference))
        self.ausgangSp_SpinBox_UEB.setValue(float(self.ueb_config.v_Bridge))
        self.softstart_checkBox_UEB.setChecked(bool(int(self.ueb_config.enableSoftstarter)))
        self.softstartD_SpinBox_UEB.setValue(float(self.ueb_config.softstartDuration))
        self.dritteHarm_checkBox_UEB.setChecked(bool(int(self.ueb_config.thridHarmonic)))
        self.operation_Mode_comboBox.setCurrentText(self.ueb_config.operationMode)
        if(bool(int(self.ueb_config.rotationDirection))):
            self.rightturn_radioButton_UEB.setChecked(True)
            self.leftturn_radioButton_UEB.setChecked(False)
        else:
            self.leftturn_radioButton_UEB.setChecked(True)
            self.rightturn_radioButton_UEB.setChecked(False)


    def sendUEBConfigTab(self):
        """sendUEBConfigTab Übertragen der GUI Einstellungen auf den Controller
        """
        self.communication.writeCommand(self.scpi_commands.setUEBRotation(self.rightturn_radioButton_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBThridHarmonic(self.dritteHarm_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartEnable(self.softstart_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartDuration(self.softstartD_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVBridge(self.versorgSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVout(self.ausgangSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBFrequency(self.frequenz_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_INIT_FINISH))

#TODO RESolver Kommandos und view
    def setResolver_Config(self, ueb_config_list):
        """setResolver_Config tdb

        Args:
            ueb_config_list (List): Liste mit Controllerparametern
        """
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
        """setResolver_Config_Tab tbd
        """
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
        """sendResolverConfigTab tbd
        """
        self.communication.writeCommand(self.scpi_commands.setResolverStatus(0xFFFF))
        self.communication.writeCommand(self.scpi_commands.setResolverLOSThreshold(self.LOS_doubleSpinBox_Resolver.value()))
        self.communication.writeCommand(self.scpi_commands.setResolverDOSOverrangeThres(self.DOS_doubleSpinBox_Resolver.value()))
        self.communication.writeCommand(self.scpi_commands.setResolverDOSMismatchThres(self.DOSMismatch_doubleSpinBox_Resolver))
        self.communication.writeCommand(self.scpi_commands.setResolverDOSResetMin(self.DOSResetMin_lineEdit_Resolver.value()))
        self.communication.writeCommand(self.scpi_commands.setResolverDOSResetMax(self.DOSResetMax_doubleSpinBox_Resolver.value()))
        self.communication.writeCommand(self.scpi_commands.setResolverLOTHighThres(self.LOTHigh_doubleSpinBox_Resolver.value()))
        self.communication.writeCommand(self.scpi_commands.setResolverLOTLowThres(self.LOTLow_doubleSpinBox_Resolver.value()))
        self.communication.writeCommand(self.scpi_commands.setResolverExcitationFreq(self.Excitation_doubleSpinBox_Resolver.value()))
        if self.PhaseLock360_radioButton_Resolver.isChecked():
            self.communication.writeCommand(self.scpi_commands.setResolverPhaseLockRange(0x0))
        else:
            self.communication.writeCommand(self.scpi_commands.setResolverPhaseLockRange(0x1))
    
        self.communication.writeCommand(self.scpi_commands.setResolverExcitationFreq(self.Excitation_doubleSpinBox_Resolver.value()))
        self.communication.writeCommand(self.scpi_commands.setResolverHysteresis(self.Hysteresis_checkBox_Resolver.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setResolverResolution(self.RDCRes_comboBox_Resolver.currentText()))


    def startMotor(self):
        """startMotor Startet die Thread für die Datenübertragung und den Motor
        """
        if ("Trennen" in self.connectComPort_Button.text() and not (len(self.parameter_list) == 0)):
            self.communication.readSerialRead()
            self.startDataProcessThread()
            self.startButton_UEB_status.setText("Motor läuft")
            self.gui_info_dialog_Label.setText("Motor gestartet")
            self.measure_run = True
            if(self.GUI_THREEPHASE in self.operation_Mode_comboBox.currentText()):
                self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_RUN_THREEPHASE))
            elif(self.GUI_DC in self.operation_Mode_comboBox.currentText()):
                self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_RUN_DC))
            elif(self.GUI_CONTROL in self.operation_Mode_comboBox.currentText()):
                self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_RUN_CONTROL))  
            elif(self.GUI_CAL_ADC in self.operation_Mode_comboBox.currentText()):
                self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_RUN_CAL_ADC))

            if(self.measureAtStartup_checkBox_UEB_status.isChecked()):
                self.startMeasure()

    def startMeasure(self):
        """startMeasure Startet die Threads für die Datenübertragung und übermittelt die einstellten IDs
        """
        if ("Trennen" in self.connectComPort_Button.text() and not (len(self.parameter_list) == 0)):
            if(self.measureAtStartup_checkBox_UEB_status.isChecked() and not self.savePath):
                self.savePathDialog()          
            self.communication.readSerialRead()
            self.startDataProcessThread()
            self.measure_run = True
            self.measure_started = True
            self.startMeasureUEBSettings_pushButton.setText("Messung läuft")
            self.gui_info_dialog_Label.setText("Messung läuft")
            if (not self.job.is_alive()):
                timer = QTimer()
                timer.timeout.connect(self.sendParameter)
                timer.setSingleShot(True)
                timer.start(2000)
            else:
                self.sendParameter()
     
    def startDataProcessThread(self):
        """startDataProcessThread Startmethode für den Thread zur Datenverarbeitung
        """
        if(not self.job.is_alive()):
            self.job = Job(interval=self.REFRESH_INTERVAL, execute=self.processData, name="DataProcessThread")
            self.job.start()

    def sendParameter(self):
        """sendParameter Übermitteln der eingestellten IDs
        """
        for i in range(0, len(self.parameter_list)):
                if(not int(self.parameter_list[i].GUI_id) == 0):                   
                    self.communication.writeCommand(self.scpi_commands.setDatatransmissionInit(self.parameter_list[i].GUI_id))   
                    self.terminalString = self.terminalString + self.scpi_commands.setDatatransmissionInit(self.parameter_list[i].GUI_id) + '\r'
        print("Max Threads verfügbar: " + str(QThreadPool.globalInstance().maxThreadCount()))

    def stopMotor(self):
        """stopMotor Stoppt den Motor
        """
        if ("Trennen" in self.connectComPort_Button.text()):
            self.communication.writeCommand(self.scpi_commands.setUEBsettings(self.UEB_STOP))
            print("Motor stop")
            self.terminalTimer.stop()
            self.startButton_UEB_status.setText("Motor starten")
            self.startMeasureUEBSettings_pushButton.setText("Messung starten")
            self.gui_info_dialog_Label.setText("Motor gestoppt")
            self.measure_run = False

    def showTransmissinoParameterDialog(self):
        """showTransmissinoParameterDialog Öffnet den Konfigurationsdialog für die Übertragungs IDs
        """
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

    def setUEBTransmissionSettingsWindow(self):
        """setUEBTransmissionSettingsWindow Beschreibt das IDs ScrollFenster in UEB Einstellungen
        """
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
        """clearLayout Leert das übergebene Layout

        Args:
            layout (Layout): Das zu leerende Layout
        """
        if layout is not None:
            while layout.count():
                childlayout = layout.takeAt(0)
                if childlayout.widget() is not None:
                    childlayout.widget().deleteLater()
                elif childlayout.layout() is not None:
                    self.clearLayout(childlayout.layout())

    def safeParameterToJSON(self):
        """safeParameterToJSON Speichert die eingestellten Übertragungsparameter in einer JSON Datei
        """
        jsonString = json.dumps([ob.__dict__ for ob in self.parameter_list])
        fileName, _ = QFileDialog.getSaveFileName(self,"Speichern unter:","","Text Files (*.json)")
        if(len(fileName) != 0):
            jsonFile = open(fileName, 'w')
            jsonFile.write(jsonString)
            jsonFile.close()
            self.gui_info_dialog_Label.setText("Einstellungen für Übertragung in Datei gespeichert")

    def loadParameterFromJSON(self):
        """loadParameterFromJSON Lädt die Übertragungsparameter aus einer JSON Datei
        """
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
                parameter.delimiter = filecontent[i]['delimiter']
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
            self.gui_info_dialog_Label.setText("Einstellungen für Übertragung aus Datei geladen")

    def safeUEBToJSON(self):
        """safeUEBToJSON Speichert die Controllerparameter in einer JSON Datei
        """
        self.setUEB_Config_from_UserInput()
        fileName, _ = QFileDialog.getSaveFileName(self,"Speichern unter:","","Text Files (*.json)")
        if(fileName):
            jsonString = json.dumps(vars(self.ueb_config))
            jsonFile = open(fileName, 'w')
            jsonFile.write(jsonString)
            jsonFile.close()
            self.gui_info_dialog_Label.setText("Einstellungen für Controller in Datei gespeichert")

    def loadUEBFromJSON(self):
        """loadUEBFromJSON Lädt die Controllerparameter aus einer JSON Datei
        """
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
            self.ueb_config.operationMode = filecontent['operationMode']
            self.setUEB_Config_Tab()
            jsonFile.close()
            self.gui_info_dialog_Label.setText("Einstellungen für Controller aus Datei importiert")


    def getParameterOfData(self, data):
        """getParameterOfData Gibt die Parameter der übergebenen Daten zurück

        Args:
            data (DataContent): Daten für die die Parameter gesucht werden sollen

        Returns:
            Parameter: Parameter Objekt mit den zu den Daten gehörigen Parametern
        """
        parameter = Parameter()
        for i in range(0, len(self.parameter_list)):
            if(str(data[0].GUI_id) in self.parameter_list[i].GUI_id):
                parameter = self.parameter_list[i]
                break
        return parameter

    def processData(self):
        """processData Threadmethode zur Datenverarbeitung der GUI
        """
        self.measure_run = self.dt_algorithmus.processQueue(self.communication.thread_data_queue)
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
    """Job Interne Klasse zur Steuerung des Datenverarbeitungsthreads

    Args:
        threading (threading.Thread): Thread
    """
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
