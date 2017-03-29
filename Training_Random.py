  #!/usr/bin/python
import spidev  # SPI interface
import time
#import firgelli
import mcp3002
import mcp3208
import RPi.GPIO as GPIO
import os
from datetime import datetime as dt
#from servo import setActuator
from lever_class import Lever

# XXX Do not run multiple instances of this program at once (or it will confuse position tracking)!

# gdrive
LOGGING = True

# Arena params
v_positions = [0.00130, 0.00120, 0.00110]
#h_positions = [0.00145, 0.00135, 0.00125, 0.00115, 0.00105]
h_positions = [0.00105, 0.00115, 0.00125, 0.00135, 0.00145]

threshold = 3200
timeout = 4  # Reward refractory period in seconds
#rewardTime = time.time()
successes = 0
tot_successes = 0
rewardTime = 0
last_arena_pos = (0, 0)

#################
# Pin definitions
#################
#pin_v_act_R = 26
#pin_h_act_R = 13
pin_v_act_L = 26  # Vertical actuator, left; 13.5% - 9.5%
pin_h_act_L = 20   # Horizontal actuator, left; 15.5% - 10%
pin_pump = 27
#pin_power = 14
pin_LED = 15
pin_v_act_manual = 13  # pin to manually advance vertical position
pin_h_act_manual = 5  # pin to manually advance horizontal position
pin_success = 14



lever_ch1 = 2 #Lever adc channel
lever_ch2 = 3
nose_ch = 7 #nosepoke adc channel

#######################################
# Initialize pins
#######################################
GPIO.setmode(GPIO.BCM)
for temp_pin in [pin_pump, pin_LED, pin_success]:
    GPIO.setup(temp_pin, GPIO.OUT)
pump = GPIO.PWM(pin_pump, 1000)
GPIO.setup(pin_v_act_manual, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#for temp_pin in [pin_power]:
#    GPIO.setup(temp_pin, GPIO.IN)
for temp_pin in [pin_v_act_manual, pin_h_act_manual]:
    GPIO.setup(temp_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create lever object
lever_obj = Lever(pin_h_act_L, pin_v_act_L, v_positions, h_positions,
                  threshold, verbose=True)
lever_obj.reset_pos()  # Move lever back to initial position
time.sleep(1.5)

# Threaded callback functions. These will execute the specified callback
# functions independent of the main loop
# XXX: THESE SEEM TO GET CALLED TWICE RANDOMLY, DON'T USE
#GPIO.add_event_detect(pin_v_act_manual, GPIO.FALLING,
#                      callback=advance_v_pos_wrapper, bouncetime=1000)
#GPIO.add_event_detect(pin_h_act_manual, GPIO.FALLING,
#                      callback=advance_h_pos_wrapper, bouncetime=1000)

# Check for power switch. MAKE SURE THIS IS ON THE RIGHT PIN
#GPIO.add_event_detect(pin_power, GPIO.RISING,
#                      callback=os.system('sudo shutdown -h now'))

####################
# Setup log file
####################
animal_number = raw_input("Input animal number and press ENTER: ")
##stim_state = raw_input("Will the animal be stimulated? Input ON or OFF and press ENTER: ")
#training_number = raw_imput("Input training step number and press ENTER: "
print('Begin training animal ' + str(animal_number))
fileName = (dt.fromtimestamp(time.time()).strftime("%y,%m,%d,%H,%M,%S")+str('_rat_')+str(animal_number)+str('_trainig_')+str('step13'))

# Make data folder if doesn't exist
try:
    os.makedirs('training')
except OSError:
    if not os.path.isdir('training'):
        raise
fileName = "training/" + fileName + ".csv"
if LOGGING:
    with open(fileName, 'w') as data_file:
        data_file.write("time,leverL,nose,threshold,horizontal,vertical,manual_lever_h,manual_lever_v,fail_push,fail_nose,success\n")


def give_reward():
    """Helper function to turn on water"""

    print("\tSuccess number %i. (%i total)" % (successes, tot_successes))
    pump.start(50)
    GPIO.output(pin_LED, True)
    GPIO.output(pin_success, True)
    time.sleep(0.3)
    GPIO.output(pin_success, False)
    GPIO.output(pin_LED, False)
    pump.stop()

####################
# Main program loop
####################
# Initialize lever and nose sensors
adc1 = mcp3208.mcp3208(0)
adc2 = mcp3208.mcp3208(1)


# Set initial position of lever/nose sensors
last_arena_pos = (adc1.readChannel(lever_ch1),adc1.readChannel(nose_ch) )

while successes < 3:
    currentTime = time.time()
    success = 0
    manual_lever_v = 0
    manual_lever_h = 0
    fail_push = 0
    fail_nose = 0
    leverL = adc1.readChannel(lever_ch1)
    nose = adc1.readChannel(nose_ch)
    # Get new data from lever and nose sensors
    #leverL, leverR = mcp3002.read(lever_sensor)
    #adc3, nose = mcp3002.read(poke_sensor)

    # Check for button press to manually advance
    v_manual_btn, h_manual_btn = GPIO.input(pin_v_act_manual), GPIO.input(pin_h_act_manual)
    if v_manual_btn == False:
        lever_obj.advance_v_pos(manual=True)
        successes = 0
        manual_lever_v = 1
        time.sleep(0.5)
    if h_manual_btn == False:
        lever_obj.advance_h_pos(manual=True)
        successes = 0
        manual_lever_h = 1
        time.sleep(0.5)
    if v_manual_btn == True:
        manual_lever_v = 0
    if h_manual_btn == True:
        manual_lever_h = 0

    # Check for successful trial
    if (leverL > lever_obj.threshold and
        nose < 100 and
        currentTime - rewardTime > timeout):
        success = 1

        successes = successes + 1
        tot_successes = tot_successes + 1
        rewardTime = time.time()
        give_reward()  # Activate pump/LED

        # Check if we need to advance to next position
        if successes >= 3:
            successes = 0
            lever_obj.advance_lever()
            time.sleep(1)  # Give time for actuators to move. Necessary?

        # Should this data only be logged on a successful trial, right?
    if (leverL > 600 and leverL <700 and nose < 100):
        fail_push = 1

    if (leverL > 700 and nose < 100):
        fail_nose = 1
    if LOGGING:
        # Check if lever or nose sensors have changed since last loop
        if (leverL, nose) != last_arena_pos:
            last_arena_pos = (leverL, nose)

            # Write data
            data_file = open(fileName, 'a')  # open file in append mode
            data_file.write(str(currentTime) + "," + str(leverL) + "," +
                            str(nose) + "," + str(threshold) + "," +
                            str(lever_obj.get_h_pos()) + "," +
                            str(lever_obj.get_v_pos()) + "," +
                            str(manual_lever_h) + "," +
                            str(manual_lever_v) + "," +
                            str(fail_push) + "," +
                            str(fail_nose) + "," +
                            str(success) +"\n")
            #print "Lever: %i\tNose: %i" % last_arena_pos
            data_file.close()

    time.sleep(0.016)
