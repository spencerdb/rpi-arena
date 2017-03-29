#!/usr/bin/python3

from Arena import *
import time
import numpy
import random
from datetime import datetime as dt

class LeverTask:
    def __init__(self, animalNumber, studyNumber):

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
        self.noseThreshold = 1000

        #servos
        self.hr = HR1
        self.vr = VR1
        self.vl = VL1
        self.hl = HL1
        self.servos = [self.hr, self.vr, self.vl, self.hl]


        #adc channels
        self.rx = LL0_CH0
        self.ry = LL0_CH1
        self.lx = RL0_CH0
        self.ly = RL0_CH1
        self.noseCH = BNC3_CH
        
        #pump
        self.pump = arena.GPIO.PWM(PUMP1)
    
        
        #Data values
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
        
        self.animalNumber = animalNumber
        self.studyNumber = studyNumber
        
        #setup logging
        ##make folder if DNE
        directory = "data/" + self.studyNumber + "/" + self.animalNumber
        try:
            os.makedirs(directory)
        except OSError:
            if not os.path.isdir(directory)
                raise
        fileName = (dt.fromtimestamp(time.time()).strftime("%y,%m,%d,%H,%M,%S"))
        self.fileName = directory + "/" + fileName
        
        

         
    def update(self):
        """update state based on arena inputs values"""
        self.leverL = self.arena.analogRead(self.lx)
        self.leverR = self.arena.analogRead(self.rx)
        self.nose = self.arena.analogRead(self.noseCH)
        nose = self.nose > noseThreshold
        timeout = 
        left = (self.leverL > self.thresholdLeft) * self.enableLeft * nose
        right = (self.leverR > self.thresholdRight) * self.enableRight * nose

        if (left or right):
            self.rewardTime = time.time()
            self.successes = self.successes + 1
            self.totalSuccesses = self.totalSuccesses + 1
            self.index = self.index + 1
            self.giveReward()
           
        if (successes >= maxSuccesses):
            """advance to next position"""
            horizontal = self.index % 5
            vertical = int(numpy.floor(self.index / 5))
            horizontal = self.hPositions(horizontal)
            vertical = self.vPositions(vertical)
            
        self.vPositions = [0.00130, 0.00120, 0.00110]
        self.hPositions = [0.00105, 0.00115, 0.00125, 0.00135, 0.00145]
            
            if (enabledRight):
                self.arena.setActuator(self.hr,horizontal)
                self.arena.setActuator(self.vr,vertical)
                
            if (enabledLeft):
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
        """Helper function to deliver pump reward"""
        self.pump.start(50) 
        self.arena.digitalWrite(self.pinLED, 1)
        self.arena.digitalWrite(self.pinSuccess, 1)
        time.sleep(0.3)
        self.arena.digitalWrite(self.pinLED, 0)
        self.arena.digitalWrite(self.pinSuccess, 0)
        self.pump.stop()
        
        
