#!/usr/bin/python
import spidev
import time


spi = spidev.SpiDev()
spi.open(0,0);
while True:
    msb = spi.xfer([0x70])
    lsb = spi.xfer([0])
    adc1 = msb[0]<<8|lsb[0]
    print adc1

