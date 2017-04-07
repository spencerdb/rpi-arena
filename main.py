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
import random

#Arena Thread class
class ArenaThread(QThread):

    trigger = pyqtSignal()
    stop = pyqtSignal()

    def __init__(self,params):
        #params [studyNumber,animalNumber,leftLever,RightLever,lEnable,rEnable,success#]
        #vars [leftLever,rightLever,success,total,time]
        self.params = params
        self.parmchange = False
        QThread.__init__(self)
        self.mutex = QMutex()
        self.running = True
        self.task = LeverTask(params)
        self.index = 0
        self.indexChanged = True
        


    def run(self):
        print('run')
        while(self.running):
            time.sleep(0.1)
            if(self.indexChanged):
                self.indexChanged = False   
                self.task.setIndex(self.index)
            if (self.parmchange):
                self.parmchange = False
                self.task.thresholdLeft = self.params[2]
                self.task.thresholdRight = self.params[3]
                self.task.enableLeft = self.params[4]
                self.task.enableRight = self.params[5]
                self.task.maxSuccesses = self.params[6]
            self.val = self.task.update()
            self.trigger.emit()
			
        
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
        successValidator = QIntValidator(0,10000, self)
        leverValidator = QIntValidator(0,4096, self)
        self.lLever.setValidator(leverValidator)
        self.rLever.setValidator(leverValidator)
        self.mSuccesses.setValidator(successValidator)
        
        self.running = False

        ##input handlers
        self.stop.clicked.connect(lambda: self.stopClicked())
        self.start.clicked.connect(lambda: self.startClicked())

        self.mButtons = [self.mButton1, self.mButton2, self.mButton3, self.mButton4, self.mButton5, self.mButton6, self.mButton7, self.mButton8, self.mButton9, self.mButton10, self.mButton11, self.mButton12, self.mButton13, self.mButton14, self.mButton15]

        self.mButtons[0].clicked.connect(lambda: self.setIndex(0))
        self.mButtons[1].clicked.connect(lambda: self.setIndex(1))
        self.mButtons[2].clicked.connect(lambda: self.setIndex(2))
        self.mButtons[3].clicked.connect(lambda: self.setIndex(3))
        self.mButtons[4].clicked.connect(lambda: self.setIndex(4))
        self.mButtons[5].clicked.connect(lambda: self.setIndex(5))
        self.mButtons[6].clicked.connect(lambda: self.setIndex(6))
        self.mButtons[7].clicked.connect(lambda: self.setIndex(7))
        self.mButtons[8].clicked.connect(lambda: self.setIndex(8))
        self.mButtons[9].clicked.connect(lambda: self.setIndex(9))
        self.mButtons[10].clicked.connect(lambda: self.setIndex(10))
        self.mButtons[11].clicked.connect(lambda: self.setIndex(11))
        self.mButtons[12].clicked.connect(lambda: self.setIndex(12))
        self.mButtons[13].clicked.connect(lambda: self.setIndex(13))
        self.mButtons[14].clicked.connect(lambda: self.setIndex(14))

        self.mReward.clicked.connect(lambda: self.giveReward())
        self.mFlush.clicked.connect(lambda: self.giveReward())
        self.mAdvance.clicked.connect(lambda: self.setIndex(random.randint(0,14)))
        
        
        self.mSet.clicked.connect(lambda: self.setParams())
        
        

        #signals

		#ui parameters
		

    #manual set button handler
    def mSetClicked(self):
        int(self.lLever.text())
        return
    
    #parameter control callbacks
    def setIndex(self,index):
        if (self.running):
            self.arenaThread.setIndex(index)

    def giveReward(self):
        if (self.running):
            self.arenaThread.task.giveReward()
    
    def setParams(self):
        if (self.running):
            self.arenaThread.params = [self.study.text(),self.animal.text(),int(self.lLever.text()),int(self.rLever.text()),bool(self.lEnable.isChecked()),bool(self.rEnable.isChecked()),int(self.mSuccesses.text())]
            self.arenaThread.parmchange = True

    #start button handler
    def startClicked(self):
        self.running = True
        self.start.setEnabled(False)
        self.arenaThread = ArenaThread([self.study.text(),self.animal.text()])
        self.arenaThread.trigger.connect(self.updateGUI)
        self.arenaThread.start()
        return
    
    #stop button handler
    def stopClicked(self):
        self.running = False
        self.arenaThread.running = False
        self.arenaThread.terminate
        self.start.setEnabled(True)
        return

    #periodically update UI from data
    def updateGUI(self):
        self.lLeverPos.display(self.arenaThread.val[0])
        self.rLeverPos.display(self.arenaThread.val[1])
        self.currentSuccess.display(self.arenaThread.val[2])
        self.totalSuccess.display(self.arenaThread.val[3])
        return


    
    
    

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
