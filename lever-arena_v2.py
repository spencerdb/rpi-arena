#!/usr/bin/python
import spidev  # SPI interface
import time
#import firgelli
import mcp3002
import RPi.GPIO as GPIO
import os
from datetime import datetime as dt
#from servo import setActuator
from lever_class import Lever

# XXX May have some scope issues with variables like rewardTime and successes

# gdrive
LOGGING = True

# Arena params
v_positions = [0.00130, 0.00120, 0.00110]
h_positions = [0.00105, 0.00115, 0.00125, 0.00135, 0.00145]
threshold = 700
timeout = 4  # Reward refractory period in seconds
#rewardTime = time.time()
successes = 0
rewardTime = 0
last_arena_pos = (0, 0)

#################
# Pin definitions
#################
#pin_v_act_R = 26
#pin_h_act_R = 13
pin_v_act_L = 19  # Vertical actuator, left; 13.5% - 9.5%
pin_h_act_L = 6   # Horizontal actuator, left; 15.5% - 10%
pin_pump = 5
pin_power = 14
pin_LED = 15
pin_v_act_manual = 23  # pin to manually advance vertical position
pin_h_act_manual = 24  # pin to manually advance horizontal position

#######################################
# Initialize pins
#######################################
GPIO.setmode(GPIO.BCM)
for temp_pin in [pin_pump, pin_LED]:
    GPIO.setup(temp_pin, GPIO.OUT)
pump = GPIO.PWM(5, 1000)

for temp_pin in [pin_power, pin_v_act_manual, pin_h_act_manual]:
    GPIO.setup(temp_pin, GPIO.IN)

# Create lever object
lever_obj = Lever(pin_v_act_L, pin_h_act_L, h_positions, v_positions,
                  threshold, verbose=True)
lever_obj.reset_pos()  # Move lever back to initial position
time.sleep(1.5)

# Threaded callback functions. These will execute the specified callback
# functions independent of the main loop
#GPIO.add_event_detect(pin_v_act_manual, GPIO.RISING,
#                      callback=lever_obj.advance_v_pos, bouncetime=250)
#GPIO.add_event_detect(pin_h_act_manual, GPIO.RISING,
#                      callback=lever_obj.advance_h_pos, bouncetime=250)

# Check for power switch. MAKE SURE THIS IS ON THE RIGHT PIN
#GPIO.add_event_detect(pin_power, GPIO.RISING,
#                      callback=os.system('sudo shutdown -h now'))

####################
# Setup log file
####################
fileName = dt.fromtimestamp(time.time()).strftime("%y,%m,%d,%H,%M,%S")

# Make data folder if doesn't exist
try:
    os.makedirs('data')
except OSError:
    if not os.path.isdir('data'):
        raise
fileName = "data/" + fileName + ".csv"
if LOGGING:
    with open(fileName, 'w') as data_file:
        data_file.write("time,leverL,nose,threshold,horizontal,vertical\n")


def give_reward():
    """Helper function to turn on water"""

    print "\tSuccess number %i." % successes
    pump.start(50)
    GPIO.output(pin_LED, True)
    time.sleep(0.3)
    GPIO.output(pin_LED, False)
    pump.stop()

####################
# Main program loop
####################
# Initialize lever and nose sensors
lever_sensor = mcp3002.init(0)
poke_sensor = mcp3002.init(1)

# Set initial position of lever/nose sensors
last_arena_pos = (mcp3002.read(lever_sensor)[0], mcp3002.read(poke_sensor)[1])

while successes < 3:
    currentTime = time.time()

    # Get new data from lever and nose sensors
    leverL, leverR = mcp3002.read(lever_sensor)
    adc3, nose = mcp3002.read(poke_sensor)

    # Check for successful trial
    if (leverL > lever_obj.threshold and
        nose < 100 and
        currentTime - rewardTime > timeout):

        successes = successes + 1
        rewardTime = time.time()
        give_reward()  # Activate pump/LED

        # Check if we need to advance to next position
        if successes >= 3:
            successes = 0
            lever_obj.advance_lever()
            time.sleep(1)  # Give time for actuators to move. Necessary?

        # Should this data only be logged on a successful trial, right?

    if LOGGING:
        # Check if lever or nose sensors have changed since last loop
        if (leverL, nose) != last_arena_pos:
            last_arena_pos = (leverL, nose)

            # Write data
            data_file = open(fileName, 'a')  # open file in append mode
            data_file.write(str(currentTime) + "," + str(leverL) + "," +
                            str(nose) + "," + str(threshold) + "," +
                            str(lever_obj.get_h_pos()) + "," +
                            str(lever_obj.get_v_pos()) + "\n")
            #print "Lever: %i\tNose: %i" % last_arena_pos
            data_file.close()

    time.sleep(0.016)