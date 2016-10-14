#!/usr/bin/python
import spidev #SPI interface
import time
import firgelli
import mcp3002
import RPi.GPIO as GPIO
import os
import datetime
import random
from servo import setActuator

#gdrive
LOGGING = True


#Pin Definition 
pump = 5
# at 100hz
verticalR = 26
verticalL = 19 # 13.5% - 9.5%
horizontalR = 13
horizontalL = 6 # 15.5% - 10%
power = 14
LED = 15


#pin setup
GPIO.setmode(GPIO.BCM)
for pin in [pump, verticalR, verticalL, horizontalR, horizontalL, LED]:
	GPIO.setup(pin, GPIO.OUT) 

GPIO.setup(power,GPIO.IN)
pump = GPIO.PWM(5,1000)

#Task parameters
timeout = 4 #time in seconds
rewardTime = time.time()
threshold = 600 #to be changed later
previousLever = 0

#State Parameters
leverL = 0
leverR = 0
nose = 0
currentTime = time.time()

#Task Parameters
successes = 0

#log file
fileName = datetime.datetime.fromtimestamp(time.time()).strftime("%y,%m,%d,%H,%M,%S")
#make data folder if doesn't exist
try:
	os.makedirs('data')
except OSError:
	if not os.path.isdir('data'):
		raise
fileName = "data/" + fileName + ".csv"
if LOGGING:
	data = open(fileName,"w")
	data.write("time,leverL,nose,threshold,horizontal,vertical\n")
	data.close()

#main program loop for non-time critical tasks
def main():
	lever = mcp3002.init(0)
	poke = mcp3002.init(1)
	rewardTime = time.time()
	resetTimer = time.time()
	resetTime = 10
	reset = False
	#reset the actuator to default position
	time.sleep(0.5)
	#Loop through vl 9.5  11.5 13.5
	# 						hl 10.5 12.0 13.5 15.0
	while True:
		for v in [0.00130, 0.00120, 0.00110]:
			setActuator(verticalL,v)
			for h in [0.00105, 0.00115, 0.00125, 0.00135, 0.00145]:
				thresholds = [700, 600]
				threshold = thresholds[random.randrange(0,2)]
				threshold = 700
				print threshold
				setActuator(horizontalL,h)
				successes = 0
				while successes < 3:
					#get new data
					[leverL,leverR] = mcp3002.read(lever) 
					[adc3,nose] = mcp3002.read(poke) 
					currentTime = time.time()

					#check for power switch
					if (GPIO.input(14) > 0):
						os.system("sudo shutdown -h now")
					
					#reset switching
					#put into function
					if leverL > 400:
						resetTimer = time.time()
						GPIO.output(LED,False)
					if leverL < 400:
						GPIO.output(LED,True)
					if (time.time() - resetTimer > resetTime):
						GPIO.output(LED,False)
						reset = True
						break
						
					if (leverL > threshold and nose < 100 and currentTime - rewardTime > timeout):
						successes = successes + 1
						rewardTime = time.time()
						#pump parameters
						pump.start(50)
						GPIO.output(LED,True)
						time.sleep(0.3)
						GPIO.output(LED,False)
						pump.stop()

					#log data if change
					if LOGGING:	
						data = open(fileName,"a")
						data.write(str(currentTime) + "," + str(leverL) + "," + str(nose) + "," + str(threshold) + "," + str(h) + "," + str(v) + "\n")	
						data.close()
					
					time.sleep(0.016)
				successes = 0
				if reset:
					break
			if reset:
				break
main()
