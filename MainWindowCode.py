import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
import RunMotor
from RunMotor import MotorThread
import threading
import minimalmodbus
import time
import serial
#import pyqtgraph as pg
#from pyqtgraph import PlotWidget, plot

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # port name, slave address (in decimal)
instrument.serial.baudrate = 9600 # set baud rate

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):                               # Must include to have things work
        super().__init__()
        self.motor_thread = MotorThread()
        self.temp_thread = TempThread()
        self.temp_thread.update.connect(self.retranslateUi)


    def setupUi(self):                                # Function to indicate placements/naming of GUI elements
        
        # Main Window Box Setup
        self.setObjectName("MainWindow")
        self.resize(700, 600)  # Initial size of popup window
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self._translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(self._translate("MainWindow", "Test Bench Menu"))

         # HTX Logo
        
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setObjectName("logo")
        self.logo.setGeometry(QtCore.QRect(150,350,700,200))
        self.logo.setPixmap(QtGui.QPixmap("HTXpic.png"))
        self.logo.setScaledContents(False)
#####################################################################################
        ## User Input for Temp Setpoint ## 
        # Label Text
        self.tempSetLabel = QLabel(self)  
        self.tempSetLabel.setText("Temp Setpoint °C:")
        self.tempSetLabel.setObjectName("tempSetLabel")
        self.tempSetLabel.setGeometry(QtCore.QRect(425, 10,150,50))
        # Dialog Box for user input
        self.tempInput = QLineEdit(self)    # Establishing object
        self.tempInput.setObjectName("tempInput")
        self.tempInput.setGeometry(QtCore.QRect(575, 10,100,50))
        # self.tempInput.returnPressed.connect(self.SendTempData)   # When you press enter, it sends to CAL
        # OK PushButton
        self.tempSend = QtWidgets.QPushButton("OK", self.centralwidget)
        self.tempSend.setGeometry(QtCore.QRect(575, 80, 100, 50))
        self.tempSend.setObjectName("tempSend")
        self.tempSend.setCheckable(False)
        
        self.tempSend.clicked.connect(self.show)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.tempSend.clicked.connect(self.SendTempData)  # Connect button to SendTempInput function

        # QC PushButtons for One Click Temp Control
        # Button 30
        self.temp1 = QtWidgets.QPushButton("30°", self.centralwidget)
        self.temp1.setGeometry(QtCore.QRect(10, 120, 100, 50))
        self.temp1.setObjectName("temp1")
        self.temp1.setCheckable(False)
        self.temp1.clicked.connect(self.show)
        self.temp1.clicked.connect(self.Send30)

        #Button50
        self.temp2 = QtWidgets.QPushButton("50°", self.centralwidget)
        self.temp2.setGeometry(QtCore.QRect(120, 120, 100, 50))
        self.temp2.setObjectName("temp2")
        self.temp2.setCheckable(False)
        self.temp2.clicked.connect(self.show)
        self.temp2.clicked.connect(self.Send50)

        #Button 80
        self.temp3 = QtWidgets.QPushButton("80°", self.centralwidget)
        self.temp3.setGeometry(QtCore.QRect(230, 120, 100, 50))
        self.temp3.setObjectName("temp3")
        self.temp3.setCheckable(False)
        self.temp3.clicked.connect(self.show)
        self.temp3.clicked.connect(self.Send80)

        # Button 175
        self.temp4 = QtWidgets.QPushButton("175°", self.centralwidget)
        self.temp4.setGeometry(QtCore.QRect(340, 120, 100, 50))
        self.temp4.setObjectName("temp4")
        self.temp4.setCheckable(False)
        self.temp4.clicked.connect(self.show)
        self.temp4.clicked.connect(self.Send175)


        # Display Current Temperature

        # Label Text
        # self.tempShowLabel = QLabel(self)  
        # self.tempShowLabel.setText("Current Temp °C:")
        # self.tempShowLabel.setObjectName("tempShowLabel")
        # self.tempShowLabel.setGeometry(QtCore.QRect(425, 175,150,50))

        self.tempDisplay = QtWidgets.QLabel(self.centralwidget)
        self.tempDisplay.setGeometry(QtCore.QRect(5, 175, 240, 50))
        self.tempDisplay.setObjectName("tempDisplay")

        font = self.font()  # New line for font change
        font.setPointSize(17) # New line for font change
        self.tempDisplay.setFont(QtGui.QFont(font))

        # Display Max Temp
        self.maxTempDisplay = QtWidgets.QLabel(self.centralwidget)
        self.maxTempDisplay.setGeometry(QtCore.QRect(5, 225, 240, 50))
        self.maxTempDisplay.setObjectName("tempDisplay")

        font = self.font()  # New line for font change
        font.setPointSize(17) # New line for font change
        self.maxTempDisplay.setFont(QtGui.QFont(font))
        
#################### Motor Button #################################
        # Motor Button Setup - ON
        self.motorButton = QtWidgets.QPushButton("Motor Start", self.centralwidget)
        self.motorButton.setGeometry(QtCore.QRect(0, 0, 200, 100))
        self.motorButton.setObjectName("motorButton")
        self.motorButton.setCheckable(False)
        
        
        self.motorButton.clicked.connect(self.show)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.motorButton.clicked.connect(self.OpenClick)  # Connect button to motor run function

        # Motor Button Setup - OFF
        self.motorButton2 = QtWidgets.QPushButton("Motor Stop", self.centralwidget)
        self.motorButton2.setGeometry(QtCore.QRect(210, 0, 200, 100))
        self.motorButton2.setObjectName("motorButton2")
        self.motorButton2.setCheckable(False)
        
        
        self.motorButton2.clicked.connect(self.show)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.motorButton2.clicked.connect(self.CloseClick)  # Connect button to motor run function
#######################################################################################################
        # Remains to be seen what this section does
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 418, 18))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
        


############# Graphing ###################
    # self.graphWidget = pg.PlotWidget(self)
    # self.graphWidget.setGeometry(QtCore.QRect(1,70,700,400))
    # self.graphWidget.setBackground([191, 189, 182])
    # self.graphWidget.setTitle("Temperature over Time", color="b", size="12pt")
    # styles = {'color':'r', 'font-size':'10pt'}
    # self.graphWidget.setLabel('left', 'Temp (°C)', **styles)
    # self.graphWidget.setLabel('bottom', 'Time (s)', **styles)
    # self.pen = pg.mkPen(color=(255, 0, 0), width = 6)

    # self._translate = QtCore.QCoreApplication.translate
    # self.setWindowTitle(self._translate("MainWindow", "QQ"))

    # self.dataPlot = self.graphWidget.plot(self.heatTime, self.Temp, pen=self.pen)

        
    # self.heatTime = []
        self.MaxTempVals = [] # initialize array
############# Threads ####################
    # Activate Motor thread
        self.motor_thread.start()
    # Activate temp reading thread
        self.temp_thread.start()
###########################################    
    def OpenClick(self):
        RunMotor.on = True
        
    def CloseClick(self):
        RunMotor.on = False

    def SendTempData(self):
        yeet = int(self.tempInput.text())
        # print(yeet)
        try:
            instrument.write_register(127,yeet,1)
        except:
            pass
        
    
    def Send30(self):
        try:
            instrument.write_register(127,30,1)
        except:
            pass
        

    def Send50(self):
        try:
            instrument.write_register(127,50,1)
        except:
            pass
    
    def Send80(self):
        try:
            instrument.write_register(127,80,1)
        except:
            pass
        
    
    def Send175(self):
        try:
            instrument.write_register(127,175,1)
        except:
            pass

    
    
    def retranslateUi(self):
        
        global data
        self.tempDisplay.setText(self._translate("MainWindow", f"Current Temp °C:  {data['currentTemp']}"))
        
        self.MaxTempVals.append(data["currentTemp"]) # Creating array of temperatures
        self.MaxTemp = max(self.MaxTempVals)
        self.maxTempDisplay.setText(self._translate("MainWindow", f"Max Temp       °C:  {self.MaxTemp}"))
        
        if self.MaxTemp > (data[f'currentTemp'] + 30): # If the MaxTemp reading is 30 deg over the current temp (indicating temp cutoff active), then
            try:
                instrument.write_register(127,20,1) # Set the setpoint very low to prevent heating loops
            except:
                pass
        # print(self.MaxTemp)
        # self.heatTime.append(data["Time"])

        # self.dataPlot.setData(self.heatTime, self.currentTemp)

class TempThread(QThread):
    update = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global data
        # heatTime = 0

        while True:
            time.sleep(1)
            #heatTime +=5
            
            try:
                calTemp = instrument.read_register(28, 1)
            except:
                pass
            data["currentTemp"] = calTemp
            
            #data["Time"] = heatTime
            self.update.emit()


# Code to actually run things
app = QApplication(sys.argv)
global data
data = {}

window = Ui_MainWindow()
window.setupUi()
window.show()
app.exec()
