"""
Arena base class for hardware abstraction of raspberry pi based training arena
Revision 1.0
@author Spencer Boyer
boyer2@uw.edu
"""
import time
import numpy
import re
try:
    import RPi.GPIO as GPIO
except:
    class GPIO: #empty class for testing code off the raspberry pi
        IN = 1
        OUT = 0
        HIGH = 1
        LOW = 0
        BCM = 11
        def setmode(mode):
            return 0
        def setup(pin, mode):
            return 0
        def output(val):
            return 0
        def input():
            return 0
        def PWM(pin, value):
            return 0
        def cleanup():
            return 0
    

class Arena:
    self.IN = GPIO.IN
    self.OUT = GPIO.OUT
    self.HIGH = GPIO.HIGH
    self.LOW = GPIO.LOW
    
    
        
    def digitalRead():
        return 0
        
    def analogRead():
        return -1
        
    def digitalWrite(pin, value):
        return 0
        
    
    def analogWrite():
        return 0
    
    def setup(pin, mode):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,mode)
        
    def __del__(self):
        GPIO.cleanup()

class LeverArena(Arena):
    
    hardware = 'Virtual'
        
    
    def __init(self):
        hl0 = [5, 8]
        vl0 = [6, 9]
        hr0 = [12, 10]
        vr0 = [13, 11]
        hl1 = [16, 12]
        vl1 = [19, 13]
        vr1 = [20, 14]
        hr1 = [26, 15]
        
        BNC0 = [2, 4]
        BNC1 = [3, 5]
        BNC2 = [14, 6]
        BNC3 = [4, 7]
                
        
    
    
    #dummy function to be replaced with spi protocol per hardware
    def analogRead(pin):
        if (type(pin) == list):
            pin = pin[1]
        for val in range(0, 16):
            analog(val) = numpy.sin(time.time()*2*numpy.pi/5.0)
            
    def __del__(self):
