import odrive
from odrive.enums import *
import sys
sys.path.append('../')
from setup import *
from motor import *
from env import *

# Find a connected ODrive (this will block until you connect one)
print("Searching for ODrives cards...")
oDrive1, oDrive2 = find_odrives()

shoulder = oDrive1.axis0
arm = oDrive2.axis1
forearm = oDrive2.axis0


# Config motors
print("Press Enter to configure motors")
input()
setup_odrive(shoulder)
setup_odrive(arm)
setup_odrive(forearm)

# Run calibration
print("Press Enter to start calibration")
input()
print("Calibrating...")
print("\tshoulder", end="")
run_calibration(shoulder)
print("\tarm", end="")
run_calibration(arm)
print("\tforearm\n")
run_calibration(forearm)


# Block motors
print("Press Enter to block motors")
input()
blocked_motor_mode(shoulder)
blocked_motor_mode(arm)
blocked_motor_mode(forearm)

pos_shoulder = 0
pos_arm = 0
pos_forearm = 0

# Run test
# print("Press Enter to run test")
# input()
# go_to_position(shoulder, pos_shoulder)
# input()
# go_to_position(arm, pos_arm)
# input()
# go_to_position(forearm, pos_forearm)
# input()

# Move 
print("Press Keyboard to move (79 shoulder, 46 arm, 13 forearm)")
input()
while True:
    key = input()
    if key == "7":
        pos_shoulder -= 5
    elif key == "9":
        pos_shoulder += 5
    elif key == "4":
        pos_arm -= 5
    elif key == "6":
        pos_arm += 5
    elif key == "1":
        pos_forearm -= 5
    elif key == "3":
        pos_forearm += 5
    elif key == "q":
        break
    else:
        print("Invalid key")
        continue
    print("shoulder:",pos_shoulder)
    print("arm:",pos_arm)
    print("forearm:",pos_forearm)
    go_to_position(shoulder, pos_shoulder)
    go_to_position(arm, pos_arm)
    go_to_position(forearm, pos_forearm)

    