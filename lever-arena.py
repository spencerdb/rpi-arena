#!/usr/bin/python
import spidev #SPI interface
import time
import firgelli
import mcp3002
import RPi.GPIO as GPIO

DEBUG = 0

#set pump pin BCM # 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
pump = GPIO.PWM(5,1000)
timeout = 4
rewardTime = time.time()

threshold = 700 #to be changed later

#main program loop for non-time critical tasks
def main():
	lever = mcp3002.init(0)
	poke = mcp3002.init(1)
	rewardTime = time.time()
	while True:
		[adc1,adc2] = mcp3002.read(lever) 
		[adc3,adc4] = mcp3002.read(poke) 
		if (DEBUG):
			print adc1, 
			print adc2,
			print adc4 
		if (adc1 > threshold and adc4 < 100 and time.time() - rewardTime > timeout):
			#GPIO.output(5,True)
			rewardTime = time.time()
			pump.start(50)
			time.sleep(0.5)
			#GPIO.output(5,False)
			pump.stop()
		time.sleep(0.100)

main()
