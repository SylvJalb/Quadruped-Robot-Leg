import sys
sys.path.append('../')
from params import *
from geometry import *
from leg import Leg, Position
from prints import fig_leg, update_fig_leg
from math import sqrt
from time import sleep
import matplotlib.pyplot as plt # install matplotlib with "pip3 install matplotlib"
import keyboard # install keyboard with "sudo pip3 install keyboard"

# Init leg object
foot_pos = Position(130, -50, -350)
my_leg = Leg(foot_pos)


# Check the lengths of the leg pieces
def get_dist(pos1, pos2):
    return sqrt((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2 + (pos1.z - pos2.z)**2)
print(get_dist(my_leg.shoulder_pos, my_leg.arm_pos))
print(get_dist(my_leg.arm_pos, my_leg.forearm_pos))
print(get_dist(my_leg.forearm_pos, my_leg.foot_pos))


# Show the figure
fig = fig_leg(my_leg)


# Move the foot position and check result
step = 5
# while not a 'q' key is pressed
while True:
    # update figure
    update_fig_leg(fig, my_leg)
    # wait for a key press
    plt.pause(0.1)
    # if a 'q' key is pressed, stop the loop
    if keyboard.is_pressed("q"):
        print("End.")
        break
    elif keyboard.is_pressed("up"):
        foot_pos.z += step
    elif keyboard.is_pressed("down"):
        foot_pos.z -= step
    elif keyboard.is_pressed("8"):
        foot_pos.y += step
    elif keyboard.is_pressed("2"):
        foot_pos.y -= step
    elif keyboard.is_pressed("4"):
        foot_pos.x -= step
    elif keyboard.is_pressed("6"):
        foot_pos.x += step
    # update foot position
    my_leg.set_foot_pos(foot_pos)