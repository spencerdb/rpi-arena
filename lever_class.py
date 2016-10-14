"""
lever_class.py

File to define the lever object
"""
import random
import RPi.GPIO as GPIO
from servo import setActuator


class Lever():
    """Lever object for rat arena"""

    def __init__(self, pin_v_act, pin_h_act, h_positions, v_positions,
                 threshold, v_pos=0, h_pos=0, verbose=False):
        """Initialize instance of Lever

        Parameters
        ----------
        pin_v_act: int
            GPIO pin for vertical actuator
        pin_h_act: int
            GPIO pin for horizontal actuator
        v_positions: list
            List of possibible vertical positions for lever
        h_positions: list
            List of possibible horizontal positions for lever
        threshold: int
            Lever threshold for success
        verbose: bool
            Whether or not to print out debugging messages

        Attributes
        ----------
        pin_v_act: int
            GPIO pin for vertical actuator
        pin_h_act: int
            GPIO pin for horizontal actuator
        h_positions: list
            List of possibible horizontal positions for lever
        v_positions: list
            List of possibible vertical positions for lever
        threshold: int
            Lever threshold for success
        v_pos: int
            Index (into v_positions) identifying current vertical position
        h_pos: int
            Index (into h_positions) identifying current horizontal position

        """

        # Assign instance variables
        self.pin_v_act = pin_v_act
        self.pin_h_act = pin_h_act
        self.h_positions = h_positions
        self.v_positions = v_positions
        self.threshold = threshold
        self.verbose = verbose

        self.v_pos = v_pos
        self.h_pos = h_pos

        # Initialize lever
        for temp_pin in [self.pin_v_act, self.pin_h_act]:
            GPIO.setup(temp_pin, GPIO.OUT)

    def advance_lever(self):
        """Advance position of lever one step"""

        # Advance only h_pos if not at maximum h_pos
        if self.h_pos < len(self.h_positions) - 1:
            self.advance_h_pos()

        # Advance both v_pos and h_pos if at maximum h_pos
        else:
            self.advance_h_pos()
            self.advance_v_pos()
        
        '''
        if self.verbose:
            print "Lever advancing to vertical: %i, horizontal: %i" % \
                (self.get_v_pos(), self.get_h_pos())
            '''

    def advance_v_pos(self, manual=False):
        """Advance vertical position one step"""
        # Update state of lever object
        self.v_pos += 1
        if self.v_pos >= len(self.v_positions):
            self.v_pos = 0

        # Actually change physical position of actuator
        setActuator(self.pin_v_act, self.v_positions[self.v_pos])
        if self.verbose:
            self.print_pos(manual)

    def advance_h_pos(self, manual=False):
        """Advance horizontal position one step"""

        # Update state of lever object
        self.h_pos += 1
        if self.h_pos >= len(self.h_positions):
            self.h_pos = 0

        # Actually change physical position of actuator
        setActuator(self.pin_h_act, self.h_positions[self.h_pos])
        if self.verbose:
            self.print_pos(manual)

    def reset_pos(self):
        """Reset vertical and horizontal position to zero"""
        self.v_pos = 0
        self.h_pos = 0
        setActuator(self.pin_v_act, self.v_positions[self.v_pos])
        setActuator(self.pin_h_act, self.h_positions[self.h_pos])

        if self.verbose:
            print "Lever positions reset."
            self.print_pos()

    def set_rand_threshold(self, thresh_opts=[600, 700]):
        """Helper set and get a random threshold."""
        self.threshold = thresh_opts[random.randrange(0, len(thresh_opts))]

        if self.verbose:
            print "Threshold set to: " + str(self.threshold)

        return self.threshold

    def get_v_pos(self):
        return self.v_positions[self.v_pos]

    def get_h_pos(self):
        return self.h_positions[self.h_pos]

    def print_pos(self, manual=False):
        """Helper to print out the current position"""
        if manual:
            print 'Row: %s, Position: %s; Manual Advance' % (self.v_pos, self.h_pos)
        else:
            print 'Row: %s, Position: %s' % (self.v_pos, self.h_pos)


