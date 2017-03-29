#!/usr/bin/env python3
#python 3 main ui handler file for lever-arena

#PyQt imports
import sys
import PyQt5
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QIntValidator
import mainwindow_auto
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from Arena import *


#general imports
import time
import os
import threading

#Arena Thread class
class ArenaThread(QThread):

    trigger = pyqtSignal()
    stop = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        self.mutex = QMutex()
        self.running = True
        self.params = [0,1]
        self.arena = Arena()
        
        #TODO move defaults to external file
        #Default values
        self.threshold = 3200
        self.v_positions = [0.00130, 0.00120, 0.00110]
        self.h_positions = [0.00105, 0.00115, 0.00125, 0.00135, 0.00145]
        self.timeout = 4
        self.requiredSuccesses = 3
        self.successes = 0
        self.pinLED = 15
        self.pinSuccess = 14  
        self.logging = True #log by default 
        
        

    def update(self):
        adc = self.arena.adc()
        print(adc)
        self.trigger.emit()
        return [-1 -1]


    def run(self):
        print('run')
        while(self.running):
            time.sleep(0.1)
            self.update()



#class for python GUI and handlers
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):

    #Configure the forms on the UI and their callbacks
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


        #validator for input
        positionValidator = QIntValidator(0,100, self)
        leverValidator = QIntValidator(0,4096, self)
        self.lLever.setValidator(leverValidator)
        self.rLever.setValidator(leverValidator)
        self.lHorizontal.setValidator(positionValidator)
        self.rHorizontal.setValidator(positionValidator)
        self.lVertical.setValidator(positionValidator)
        self.rVertical.setValidator(positionValidator)

        ##input handlers
        self.mSet.clicked.connect(lambda: self.mSetClicked())
        self.stop.clicked.connect(lambda: self.stopClicked())
        self.start.clicked.connect(lambda: self.startClicked())

        #signals

    #manual set button handler
    def mSetClicked(self):
        int(self.lLever.text())
        return


    #start button handler
    def startClicked(self):
		## TODO start logging
        self.start.setEnabled(False)
        self.arenaThread = ArenaThread()
        self.arenaThread.trigger.connect(self.updateGUI)
        self.arenaThread.start()
        return
    
    #stop button handler
    def stopClicked(self):
		## TODO stop logging
        self.arenaThread.running = False
        self.arenaThread.terminate
        self.start.setEnabled(True)
        return

    #periodically update UI from data
    def updateGUI(self):
        return


    
    
    

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
