"""
Control class for lever arena board revision 2.7
Revision 1.0
@author Spencer Boyer
boyer2@uw.edu
"""
import time
import numpy
import re
import servo
import RPi.GPIO as GPIO

class LeverArena27(Arena):
    
    hardware = '2.7'
        
    
    def __init(self):
       	from mcp3208 import mcp3208 
	adc0 = mcp3208(0)
	adc1 = mcp3208(1)	
	
        #actuators [pwm pin, adc channel]
        HL0 = [5, 8]
        VL0 = [6, 9]
        HR0 = [12, 10]
        VR0 = [13, 11]
        HL1 = [16, 12]
        VL1 = [19, 13]
        VR1 = [20, 14]
        HR1 = [26, 15]
        
	#BNC [digital out pin, adc channel]
        BNC0 = [2, 4]
        BNC1 = [3, 5]
        BNC2 = [14, 6]
        BNC3 = [4, 7]
	
	#Sensors
	LL0 = [2,3]
	RL0 = [0,1]
	LL1 = [4,5]
	RL1 = [6,7]
        
	#auxilary digital IO 
        aux0 = [24]
        aux1 = [21]
        aux2 = [23]
        aux3 = [25]
		
        
    
            
    def __del__(self):
        GPIO.cleanup()
