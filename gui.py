import pyqtgraph as pg

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QPushButton
from PyQt6.QtGui import QIcon
from pyqtgraph import PlotWidget, plot
from qt_material import apply_stylesheet
from ui_MainWindow import Ui_MainWindow
from ueb_config import ueb_config
from communication import Communication
from scpi_commands import scpi_commands


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    hour = [1,2,3,4,5,6,7,8,9,10]
    temperature = [30,32,34,32,33,31,29,32,35,45]
    savePath = ""

    communication = Communication()
    ueb_config = ueb_config()
    ueb_config_list = list
    scpi_commands = scpi_commands

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.scpi_commands = scpi_commands()
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
        # portlist = self.comport.getComPorts()
        self.comPort_comboBox.clear()
        self.comPort_comboBox.addItems(self.communication.getComPorts())
        # self.comPort_comboBox.setCurrentText("Comport")

    def exitButtonClicked(self):
        
        self.close()
        
    def stopButtonClicked(self):
        print("STOP")

    def connectButtonClicked(self):
        comport = self.comPort_comboBox.currentText()
        if(len(comport) != 0):
            if(self.communication.setComPort(comport)):
                print("Comport SET" + comport)
                settings = self.communication.readSettings()
                # print(settings)
                self.ueb_config_list = self.getUEB_SettingVars(settings)
                self.setUEB_Config(self.ueb_config_list)
                self.setUEB_Config_Tab()
                self.connectComPort_Button.setText("Disconnect")
            else:
                self.connectComPort_Button.setText("Connect")

    def readUEB_SettingsButtonClicked(self):
        if ("Disconnect" in self.connectComPort_Button.text()):
            settings = self.communication.readSettings()
            self.ueb_config_list = self.getUEB_SettingVars(settings)
            self.setUEB_Config(self.ueb_config_list)
            self.setUEB_Config_Tab()

    def writeUEB_SettingsButtonClicked(self):
            self.sendUEBConfigTab()

    def getUEB_SettingVars(self, settingsstring):
        parameters = settingsstring.split(";")
        for i in range(len(parameters)):
            temp = parameters[i].split("=")
            parameters[i] = temp[1]
            # print(parameters)
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
        # if(self.rightturn_radioButton_UEB.isChecked()):
        #     self.communication.writeCommand(self.scpi_commands.setUEBRotation(self.rightturn_radioButton_UEB.isChecked()))
        # else:
        #     self.communication.writeCommand(self.scpi_commands.setUEBRotation(self.leftturn_radioButton_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBRotation(self.rightturn_radioButton_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBThridHarmonic(self.dritteHarm_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartEnable(self.softstart_checkBox_UEB.isChecked()))
        self.communication.writeCommand(self.scpi_commands.setUEBSoftstartDuration(self.softstartD_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVBridge(self.versorgSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBVout(self.ausgangSp_SpinBox_UEB.value()))
        self.communication.writeCommand(self.scpi_commands.setUEBFrequency(self.frequenz_SpinBox_UEB.value()))

