#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import spidev #SPI 

#state variables
running = True
count = 0

#Pin Definitions
pump = 5
verticalR = 26
verticalL = 19
horizontalR = 13 
horizontalL = 6 

#open file for writing
dataFile = open('debug.csv', 'w')
dataFile.write('1,1\n2,2\n3,3\n4,4\n')

#initialize GPIO pins for linear actuators 
GPIO.setmode(GPIO.BCM)
for pin in [pump, verticalR, verticalL, horizontalR, horizontalL]:
    GPIO.setup(pin, GPIO.OUT)
horizontalRP = GPIO.PWM(horizontalR, 20)

horizontalRP.start(2)
time.sleep(5)
horizontalRP.ChangeDutyCycle(2.2)
time.sleep(5)
horizontalRP.stop()
# function to read from the mcp3002
def readMCP3002(device):
     
    spi = spidev.SpiDev(0,0)
    spi.open(0,device)
    msb = spi.xfer([0x70]) #ADC channel 1
    lsb = spi.xfer([0])
    adc1 = msb[0]<<8|lsb[0]
    msb = spi.xfer([0x60]) #ADC channel 2
    lsb = spi.xfer([0])
    adc2 = msb[0]<<8|lsb[0]
    spi.close()
    return [adc1,adc2]

# main loop for motor control etc
try:
    while running:
        [leftLever, rightLever] = readMCP3002(0)
        print leftLever,
        print rightLever,
        print count
        time.sleep(0.002)
        count = (count + 1)% 5000


except KeyboardInterrupt:
    GPIO.cleanup()
    dataFile.close()

