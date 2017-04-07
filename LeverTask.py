#!/usr/bin/python3

from Arena import *
import time
import numpy
import random
from datetime import datetime as dt
import os
import threading

class LeverTask:
    def __init__(self, params):
		#params [studyNumber,animalNumber,leftLever,RightLever,lEnable,rEnable,success#]
	
        self.animalNumber = params[1]
        self.studyNumber = params[0]

        #Arena handling class
        self.arena = Arena()

        #Parameters
        self.vPositions = [0.00130, 0.00120, 0.00110]
        self.hPositions = [0.00105, 0.00115, 0.00125, 0.00135, 0.00145]
        self.thresholdLeft = 3200
        self.thresholdRight = 3200
        self.timeout = 4
        self.maxSuccesses = 3
        self.enableLeft = False
        self.enableRight = True
        self.noseThreshold = 100

        #servos
        self.hr = HR1
        self.vr = VR1
        self.vl = VL1
        self.hl = HL1
        self.servos = [self.hr, self.vr, self.vl, self.hl]


        #adc channels
        self.ly = LL0_CH0
        self.lx = LL0_CH1
        self.ry = RL0_CH0
        self.rx = RL0_CH1
        self.noseCH = BNC3_CH
        
        #pump
        self.pump = GPIO.PWM(PUMP1,1000)
    
        
        #Data values
        self.time = time.time()
        self.leverL = 0
        self.leverR = 0
        self.nose = 0
        self.index = 0
        self.successes = 0
        self.totalSuccesses = 0
        self.reward = 0
        self.rewardTime = -4

        #io
        self.pinLED = 15
        self.pinSuccess = 14
        
        
        #setup logging
        ##make folder if DNE
        directory = "data/" + self.studyNumber + "/" + self.animalNumber
        try:
            os.makedirs(directory)
        except OSError:
            if not os.path.isdir(directory):
                raise
        fileName = (dt.fromtimestamp(time.time()).strftime("%y,%m,%d,%H,%M,%S"))
        self.fileName = directory + "/" + fileName
        with open(self.fileName, 'w') as data_file:
            data_file.write("time,leverL,leverR,nose,thresholdL,thresholdR,horizontal,vertical,success\n") 
        self.updatePosition()
        
         
    def update(self):
        """update state based on arena inputs values"""
        oldNose = self.nose
        oldLeverL = self.leverL
        oldLeverR = self.leverR
        self.time = time.time()
        self.leverL = self.arena.analogRead(self.ly)
        self.leverR = self.arena.analogRead(self.ry)
        self.nose = self.arena.analogRead(self.noseCH)
        self.nose = self.nose < self.noseThreshold
        nose = self.nose
        timeout = self.time > self.rewardTime
        left = (self.leverL >= self.thresholdLeft) * self.enableLeft * nose * timeout
        right = (self.leverR >= self.thresholdRight) * self.enableRight * nose * timeout
        success = left or right 

        if (success):
            self.rewardTime = time.time() + self.timeout
            self.successes = self.successes + 1
            self.totalSuccesses = self.totalSuccesses + 1
            self.giveReward()
           
        if (self.successes >= self.maxSuccesses):
            self.setIndex(random.randint(0,14))
            self.updatePosition()
            
        """log data"""
        if ( self.nose != oldNose or self.leverL != oldLeverL or self.leverR != oldLeverR ):
            """log on change"""
            dataFile = open(self.fileName, 'a') #open in append mode
            dataFile.write(str(self.time) + "," + str(self.leverL) + "," + 
                           str(self.leverR) + "," + str(self.nose) + "," +
                           str(self.thresholdLeft * self.enableLeft) + "," +
                           str(self.thresholdRight * self.enableRight) + "," +
                           str(self.hPositions[self.index % 5]) + "," + 
                           str(self.vPositions[int(numpy.floor(self.index / 5))]) + "," +
                           str(success) + "\n")
            dataFile.close()
                        
		#return vars [leftLever, rightLever, success, total,time]
        return [self.leverL, self.leverR, self.successes, self.totalSuccesses]
    

    def setIndex(self,index):
        if index == self.index:
            return
        self.index = index
        self.updatePosition()
    def updatePosition(self):
        """advance to next position"""
        self.successes = 0
        horizontal = self.index % 5
        vertical = int(numpy.floor(self.index / 5))
        horizontal = self.hPositions[horizontal]
        vertical = self.vPositions[vertical]

        if (self.enableRight):
            self.arena.setActuator(self.hr,horizontal)
            self.arena.setActuator(self.vr,vertical)
            
        if (self.enableLeft):
            self.arena.setActuator(self.hl,horizontal)
            self.arena.setActuator(self.vl,vertical)
    
        
    def setPosition(self,lv,lh,rv,rh):
        """function to set actuators to new position
        """
        self.arena.setActuator(self.vr,rv)
        self.arena.setActuator(self.hr,rh)
        self.arena.setActuator(self.vl,lv)
        self.arena.setActuator(self.hl,lh)

        
    def giveReward(self):
        """helper function to deliver reward in separate thread"""
        pumpThread = threading.Thread(target=self.giveRewardThread)
        pumpThread.start()

    def giveRewardThread(self):
        """Helper function to deliver pump reward"""
        self.pump.start(50) 
        self.arena.digitalWrite(self.pinLED, 1)
        self.arena.digitalWrite(self.pinSuccess, 1)
        time.sleep(0.3)
        self.arena.digitalWrite(self.pinLED, 0)
        self.arena.digitalWrite(self.pinSuccess, 0)
        self.pump.stop()
        
if __name__ == "__main__":
    a = LeverTask("test","-1")
    while True:
        print(a.update())
        time.sleep(0.1)
