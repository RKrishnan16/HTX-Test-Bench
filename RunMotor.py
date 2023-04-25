import RPi.GPIO as GPIO
import time
from PyQt5.QtCore import QThread, pyqtSignal
import threading



class MotorThread(QThread):
    update = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        global on 
        on = False

    def run(self):
        GPIO.setmode(GPIO.BOARD)

        ControlPin = [7,11,13,15]

        for pin in ControlPin:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin,0)
        
        seq=[ [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1] ]

        while True:

            if on:
                
                for halfstep in range(8):
                    for pin in range(4):
                        GPIO.output(ControlPin[pin], seq[halfstep][pin])
                    time.sleep(0.001)  # can modify this parameter for speed
            
            

        GPIO.cleanup()
    
