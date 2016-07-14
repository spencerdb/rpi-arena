#!/usr/bin/python

#Raspberry pi includes
import RPi.GPIO as GPIO
import time
import spidev #SPI 

#Google Drive imports
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#initialize Google Drive Credentials and connect
oauthfile = 'lever-arena-01-d2618fc356b1.json'
scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(oauthfile,scope)
gauth = GoogleAuth()
gauth.credentials = credentials
gauth.Authorize()
drive = GoogleDrive(gauth)
#TODO ensure continued program function if google drive doesn't load

#Create new file to log data to
dataFile = open('debug.csv', 'w') #open file for writing
driveFile = drive.CreateFile({'parents' : [{'id' : '0B8LTj-6zmvAPQTZZS2tSaXR4UTA'}],'title': 'debug.csv'})


#state variables
running = True
count = 0

#Pin Definitions
pump = 5
verticalR = 26
verticalL = 19
horizontalR = 13 
horizontalL = 6 


#initialize GPIO pins for linear actuators 
GPIO.setmode(GPIO.BCM)
for pin in [pump, verticalR, verticalL, horizontalR, horizontalL]:
    GPIO.setup(pin, GPIO.OUT)
horizontalRP = GPIO.PWM(horizontalR, 20)

#horizontalRP.start(2.2)
#time.sleep(5)
#horizontalRP.ChangeDutyCycle(2)
#time.sleep(5)
#horizontalRP.stop()

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

start = time.time()
# main loop for motor control etc
try:
    while running:
        now = round((time.time()-start) * 1000,2)
        [leftLever, rightLever] = readMCP3002(0)
        dataFile.write("," + repr(leftLever) + "," + repr(rightLever)+ "\n")
        dataFile.write(repr(now)) #time ms
      
        print leftLever,
        print rightLever,
        print now
        time.sleep(0.001)
        count = (count + 1) % 5000


except KeyboardInterrupt:
    GPIO.cleanup()
    dataFile.close()

