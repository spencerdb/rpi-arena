#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
pump = GPIO.PWM(5,1000)

pump.start(75)
time.sleep(5)
pump.stop()
