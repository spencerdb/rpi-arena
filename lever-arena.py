#!/usr/bin/python
import spidev #SPI interface
import time
import firgelli
import mcp3002
import RPi.GPIO as GPIO
import os
import datetime

#gdrive
LOGGING = False


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
vr = GPIO.PWM(26,100)
vl = GPIO.PWM(19,100)
hr = GPIO.PWM(13,100)
hl = GPIO.PWM(6,100)

GPIO.setup(power,GPIO.IN)
pump = GPIO.PWM(5,1000)

#Task parameters
timeout = 4 #time in seconds
rewardTime = time.time()
threshold = 700 #to be changed later

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
	data.write("time,leverL,leverR,nose")
	data.close()

def setActuator(actuator, duty):
	actuator.ChangeFrequency(100)
	actuator.start(duty)
	actuator.ChangeDutyCycle(duty)
	time.sleep(5)
	actuator.stop()
	

#main program loop for non-time critical tasks
def main():
	lever = mcp3002.init(0)
	poke = mcp3002.init(1)
	rewardTime = time.time()
	#reset the actuator to default position
	setActuator(hl,13.5)
	setActuator(vl,12)
	#Loop through vl 9.5  11.5 13.5
	# 						hl 10.5 12.0 13.5 15.0
	while True:
		#get new data
		[leverL,leverR] = mcp3002.read(lever) 
		[adc3,nose] = mcp3002.read(poke) 
		if nose < 100:
			nose = 0
		else:
			nose = 1
		currentTime = time.time()

		#check for power switch
		if (GPIO.input(14) > 0):
			os.system("sudo shutdown -h now")

		if (leverL > threshold and nose < 100 and currentTime - rewardTime > timeout):
			rewardTime = time.time()
			pump.start(50)
			GPIO.output(LED,True)
			time.sleep(0.5)
			GPIO.output(LED,False)
			pump.stop()
	
		#log data if change
		if LOGGING:	
			data = open(fileName,"a")
			data.write(str(currentTime) + "," + str(leverL) + "," + str(leverR) + "," + str(nose))	
			data.close()
		
		time.sleep(0.05)
		
main()
