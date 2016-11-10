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
from mcp3208 import mcp3208 

hardware = '2.7'

#pin definitions
#actuators
HL0_PIN = 5
HL0_CH = 15
VL0_PIN = 6
VL0_CH = 14
HR0_PIN = 12
HR0_CH = 13
VR0_PIN = 13
VR0_CH = 12
HL1_PIN = 16
HL1_CH = 11
VL1_PIN = 19
VL1_CH = 10
VR1_PIN = 20
VR1_CH = 9
HR1_PIN = 26
HR1_CH = 8

#BNC 
BNC0_PIN = 2
BNC0_CH = 4
BNC1_PIN = 3
BNC1_CH = 5
BNC2_PIN = 14
BNC2_CH = 6
BNC3_PIN = 4
BNC3_CH = 7



#Sensors
LL0_CH0 = 2
LL0_CH1 = 3
RL0_CH0 = 0
RL0_CH1 = 1
LL1_CH0 = 4
LL1_CH1 = 5
RL1_CH0 = 6
RL1_CH1 = 7


#pump pins
PUMP0 = 17
PUMP1 = 27

#pin definitions 
HIGH = 1
LOW = 0

class LeverArena27:


	def __init__(self):
		
		#initialize ADCs 	
		self.adc0 = mcp3208(0)
		self.adc1 = mcp3208(1)	

		#initialize digital pins
		GPIO.setmode(GPIO.BCM)
		
		#default all pins to output LOW
		for pin in [HL0_PIN, VL0_PIN, HR0_PIN, VR0_PIN, HL1_PIN, VL1_PIN, VR1_PIN, HR1_PIN, BNC0_PIN, BNC1_PIN, BNC2_PIN, BNC3_PIN, PUMP0, PUMP1]:
			GPIO.setup(pin,GPIO.OUT)	
			GPIO.output(pin,GPIO.LOW)

		#actuator ADC values
		self.HL0 = -1
		self.VL0 = -1
		self.HR0 = -1
		self.VR0 = -1
		self.HL1 = -1
		self.VL1 = -1
		self.VR1 = -1
		self.HR1 = -1

		#BNC  ADC/digital values
		self.BNC0 = -1
		self.BNC1 = -1
		self.BNC2 = -1 
		self.BNC3 = -1

		#Sensors ADC values
		self.LL0_0 = -1
		self.LL0_1 = -1
		self.RL0_0 = -1
		self.RL0_1 = -1
		self.LL1_0 = -1
		self.LL1_1 = -1
		self.RL1_0 = -1
		self.RL1_1 = -1

		#auxilary digital IO 
		self.aux0 = -1
		self.aux1 = -1
		self.aux2 = -1
		self.aux3 = -1

		#pump pins
		self.pump0 = -1
		self.pump1 = -1
			
	#return the digital value of pin
	def digitalRead(self,pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin,GPIO.IN)
		return GPIO.input(pin)

		
	#write pin to either high 1 or low 0
	def digitalWrite(self,pin,val):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin,GPIO.OUT)
		if val == 1:
			GPIO.output(pin,GPIO.HIGH)
		else:
			GPIO.output(pin,GPIO.LOW)
			
		
	#return 12bit analog value of channel from approrpiate adc
	def analogRead(self,channel):
		if channel < 8:	
			return self.adc0.readChannel(channel % 8)
		return self.adc1.readChannel(channel % 8)
		
	#update all analog values from hardware 
	def updateAnalog(self):
		#read adcs	        
		[self.RL0_0, self.RL0_1, self.LL0_0, self.LL0_1, self.LL1_0, self.LL1_1, self.RL1_0, self.RL1_1] = self.adc0.readADC()
		[self.HR1, self.VR1, self.VL1, self.HL1, self.VR0, self.HR0, self.VL0, self.HL0] = self.adc1.readADC()

			
	def pwm(self, pin, ms, hz=50):
			
		
        #clean up GPIO 
	def __del__(self):
		GPIO.cleanup()
