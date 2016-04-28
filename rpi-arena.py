#!/usr/bin/python
import spidev
import time
import thread
import RPi.GPIO as GPIO

#main program loop for non-time critical tasks
def main():
	while True:
		[adc1,adc2] = analogReadSPI(0)
		print adc1, 
		print adc2

def analogReadSPI(device):

	spi = spidev.SpiDev()
	spi.open(0,device)
	msb = spi.xfer([0x70]) #ADC channel 2
	lsb = spi.xfer([0])
	adc1 = msb[0]<<8|lsb[0]
	msb = spi.xfer([0x60]) #ADC channel 2
	lsb = spi.xfer([0])
	adc2 = msb[0]<<8|lsb[0]
	spi.close()
	return [adc1,adc2]

def quit()
	spi.close()
	GPI.output(2, False)
	
#initialize script
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.output(2, True)
main()
