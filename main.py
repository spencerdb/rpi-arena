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


#general imports
import time
import os
import threading
from LeverTask import *

#Arena Thread class
class ArenaThread(QThread):

    trigger = pyqtSignal()
    stop = pyqtSignal()

    def __init__(self,studyNumber,animalNumber):
        QThread.__init__(self)
        self.mutex = QMutex()
        self.running = True
        self.task = LeverTask(str(studyNumber),str(animalNumber))
        self.index = 0
        self.indexChanged = True
        


    def run(self):
        print('run')
        while(self.running):
            time.sleep(0.1)
            if(self.indexChanged):
                self.indexChanged = False   
                self.task.setIndex(self.index)
            print(self.task.update()) 
        
    def setIndex(self,index):
        self.indexChanged = True
        self.index = index



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
		
        self.mButtons = [self.mButton1, self.mButton2, self.mButton3, self.mButton4, self.mButton5, self.mButton6, self.mButton7, self.mButton8, self.mButton9, self.mButton10, self.mButton11, self.mButton12, self.mButton13, self.mButton14, self.mButton15]
        self.mButtons[0].clicked.connect(lambda: self.arenaThread.setIndex(0))
        self.mButtons[1].clicked.connect(lambda: self.arenaThread.setIndex(1))
        self.mButtons[2].clicked.connect(lambda: self.arenaThread.setIndex(2))
        self.mButtons[3].clicked.connect(lambda: self.arenaThread.setIndex(3))
        self.mButtons[4].clicked.connect(lambda: self.arenaThread.setIndex(4))
        self.mButtons[5].clicked.connect(lambda: self.arenaThread.setIndex(5))
        self.mButtons[6].clicked.connect(lambda: self.arenaThread.setIndex(6))
        self.mButtons[7].clicked.connect(lambda: self.arenaThread.setIndex(7))
        self.mButtons[8].clicked.connect(lambda: self.arenaThread.setIndex(8))
        self.mButtons[9].clicked.connect(lambda: self.arenaThread.setIndex(9))
        self.mButtons[10].clicked.connect(lambda: self.arenaThread.setIndex(10))
        self.mButtons[11].clicked.connect(lambda: self.arenaThread.setIndex(11))
        self.mButtons[12].clicked.connect(lambda: self.arenaThread.setIndex(12))
        self.mButtons[13].clicked.connect(lambda: self.arenaThread.setIndex(13))
        self.mButtons[14].clicked.connect(lambda: self.arenaThread.setIndex(14))
        #signals

    #manual set button handler
    def mSetClicked(self):
        int(self.lLever.text())
        return


    #start button handler
    def startClicked(self):
		## TODO start logging
        self.start.setEnabled(False)
        self.arenaThread = ArenaThread(self.study.text(),self.animal.text())
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
