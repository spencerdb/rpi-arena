"""
Control class for lever arena board revision 2.7
Revision 1.0
@author Spencer Boyer
boyer2@uw.edu
"""
import time
import numpy
import re
import RPi.GPIO as GPIO
from mcp3208 import mcp3208 
import threading



#pin definitions
#actuators
HL0 = 5
HL0_CH = 15
VL0 = 6
VL0_CH = 14
HR0 = 13
HR0_CH = 13
VR0 = 12
VR0_CH = 12
HL1 = 16
HL1_CH = 11
VL1 = 19
VL1_CH = 10
VR1 = 20
VR1_CH = 9
HR1 = 26
HR1_CH = 8

#BNC 
BNC0 = 2
BNC0_CH = 4
BNC1 = 3
BNC1_CH = 5
BNC2 = 14
BNC2_CH = 6
BNC3 = 4
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

class Arena:


	def __init__(self):
		
		#hardware revision	
		self.hardware = '2.7'

		#initialize ADCs 	
		self.adc0 = mcp3208(0)
		self.adc1 = mcp3208(1)	

		#initialize digital pins
		GPIO.setmode(GPIO.BCM)
		
		#default all pins to output LOW
		for pin in [HL0, VL0, HR0, VR0, HL1, VL1, VR1, HR1, BNC0, BNC1, BNC2, BNC3, PUMP0, PUMP1]:
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

	#set actuator at pin to 0.001<time<0.002
	def setActuator(self, pin, time):
		actuatorThread = threading.Thread(target = self.setActuatorThread, args = (pin,time))
		actuatorThread.start()		
		return 0

	def setActuatorThread(self,pin,delay):
		start = time.time()
		current = time.time()
		while current - start < 1:
			self.digitalWrite(pin,1)	
			time.sleep(delay)
			self.digitalWrite(pin,0)
			time.sleep(0.05)
			current = time.time()
		
	def setAcuatorPercent(self, pin, percent):
		if percent > 100:
			return -1
		time = ((percent / 100000) + 0.001)
		self.setActuator(pin, time)
		return 0

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
	def adc(self):
		#read adcs	        
		[self.RL0_0, self.RL0_1, self.LL0_0, self.LL0_1, self.LL1_0, self.LL1_1, self.RL1_0, self.RL1_1] = self.adc0.readADC()
		[self.HR1, self.VR1, self.VL1, self.HL1, self.VR0, self.HR0, self.VL0, self.HL0] = self.adc1.readADC()
		return [self.RL0_0, self.RL0_1, self.LL0_0, self.LL0_1, self.LL1_0, self.LL1_1, self.RL1_0, self.RL1_1, self.HR1, self.VR1, self.VL1, self.HL1, self.VR0, self.HR0, self.VL0, self.HL0]

			
	def pwm(self, pin, ms, hz=50):
		return 0
		
        #clean up GPIO 
	def __del__(self):
		GPIO.cleanup()
