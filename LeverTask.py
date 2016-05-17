#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import spidev #SPI 

#state variables
running = True

#start
def start():
    main()

# main loop for motor control etc
def main():
    while running:
        [leftLever, rightLever] = readMCP3002(0)
        print leftLever,
        print rightLever
        time.sleep(0.002)

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
               
#call start and begin running
if __name__ == "__main__"
    start()
