"""
Arena base class for hardware abstraction of raspberry pi based training arena
Revision 1.0
@author Spencer Boyer
boyer2@uw.edu
"""
import time
import numpy
import re
import servo.py

try:
    import spidev
except:
    class spi: #dummy class for running off of the raspberry pi
        def __init__(self):
            return 0


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
            
#holds the data for one actuator
class Actuator:
    #min/max in ms
    maxPoint = 2.0
    minPoint = 1.0
    
    pin = -1
    channel = -1
    value = -1
    setPoint = 1.5
    def __init__(self, pin, channel):
        self.pin = pin
        self.channel = channel
    def setPercent(percent):
        setPoint = (percent / 100 + 1.0)
    
    

class Arena:
    self.IN = GPIO.IN
    self.OUT = GPIO.OUT
    self.HIGH = GPIO.HIGH
    self.LOW = GPIO.LOW
    
    def setActuator(n,s):
        servo.setActuator(n,s)
        
    def digitalRead():
        return -1
        
    def analogRead():
        return -1
        
    def digitalWrite(pin, value):
        return -1
        
    
    def analogWrite():
        return -1
    
    def setup(pin, mode):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,mode)
        
    def __del__(self):
        GPIO.cleanup()

class LeverArena27(Arena):
    
    hardware = '2.7'
        
    
    def __init(self):
        
        #actuators [pwm pin, adc channel]
        hl0 = Actuator(5, 8)
        vl0 = Actuator(6, 9)
        hr0 = Actuator(12, 10)
        vr0 = Actuator(13, 11)
        hl1 = Actuator(16, 12)
        vl1 = Actuator(19, 13)
        vr1 = Actuator(20, 14)
        hr1 = Actuator(26, 15)
        
        BNC0 = [2, 4]
        BNC1 = [3, 5]
        BNC2 = [14, 6]
        BNC3 = [4, 7]
        
        aux0 =
        aux1 =
        aux2 =
        aux3 =
                
        
    
    
    #dummy function to be replaced with spi protocol per hardware
    def analogRead(channel):
        if (type(channel) == list):
            channel = channel[1]
        for val in range(0, 16):
            analog(val) = numpy.sin(time.time()*2*numpy.pi/5.0)
            
    def __del__(self):
        GPIO.cleanup()