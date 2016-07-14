#!/usr/bin/python

#initialize linear actuator on pin and return handle to pwm
def init(pin):
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin,GPIO.OUT)
	actuator = GPIO.PWM(pin, 20) #firgelli actuators take standard hobby servo
	return actuator

def initialize(pin1, pin2, pin3, pin4):
	return [init(pin1), init(pin2), init(pin3), init(pin4)]

