from params import *
from setup import *

# Motor class
class Motor:
    def __init__(self, position_name, axis):
        """
        Initialize the motor
        position_name : the name of the motor position in leg (Shoulder, Arm, Forearm)
        axis : the odrive axis to acces to the motor
        """
        self.position_name = position_name
        self.axis = axis
    
    def setup(self):
        print("Setup {name} :".format(name = self.position_name))
        setup_odrive(self.axis)
        print("\tCalibrating...")
        run_calibration(self.axis)
        print("\tCalibration done")
        blocked_motor_mode(self.axis)
        print("\tMotor blocked")

    def go_to_position(self, deg):
        """
        Go to a position in deg.
        """
        print("Go to position: {}°".format(deg))
        self.axis.controller.input_pos = deg / 360 / REDUCTION_COEF