import odrive
from odrive.enums import *
import time
import math



# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
# my_drive = odrive.find_any("serial:/dev/ttyUSB0")



# my_drive.config.enable_ascii_protocol_on_usb


# my_drive.axis0.controller.config.vel_limit = 2
# my_drive.axis0.encoder.config.cpr = 4000
# my_drive.axis0.motor.config.pole_pairs = 20
# my_drive.axis0.motor.config.current_lim = 20
# my_drive.axis0.motor.config.torque_constant = 0.0827
# my_drive.axis0.config.startup_motor_calibration = False
# my_drive.axis0.config.startup_encoder_index_search = False
# my_drive.axis0.config.startup_encoder_offset_calibration = False
# my_drive.axis0.config.startup_closed_loop_control = False
# my_drive.axis0.config.startup_sensorless_control = False
# my_drive.axis0.encoder.config.use_index = False

# my_drive.save_configuration()

# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")


# my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE


my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL


my_drive.axis0.controller.input_pos = 10
