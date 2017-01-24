"""
Script for running the pellet dispenser from the raspberry pi lever-arena r2.7
Revision 1.0
@author Spencer Boyer
boyer2@uw.edu
"""
#!/usr/bin/env python
from Arena import *

#AUX pin definitions
AUX0 = 24
AUX1 = 21
AUX2 = 23
AUX3 = 25

#easy stepper definitions
stp  = AUX1 #purple
dire = AUX3 #blue
MS2  = AUX0 #gray
MS1  = HR1  #gray
EN   = AUX2 #black

#stepper motor functions 
def resetEDPins():
	pi.digitalWrite(stp, 0)
	pi.digitalWrite(dire, 0)
	pi.digitalWrite(MS1, 0)
	pi.digitalWrite(MS2, 0)
	pi.digitalWrite(EN, 1)

def stepForward(steps):
	pi.digitalWrite(dire, 0)
	pi.digitalWrite(EN, 0)
	for x in range(0, steps):
		pi.digitalWrite(stp, 1)
		time.sleep(0.001)
		pi.digitalWrite(stp, 0)
		time.sleep(0.001)
	pi.digitalWrite(EN, 1)

pi = Arena()
resetEDPins()
pi.digitalWrite(MS1, 1)
pi.digitalWrite(MS2, 1)
pi.digitalWrite(EN, 0)
stepForward(800)

