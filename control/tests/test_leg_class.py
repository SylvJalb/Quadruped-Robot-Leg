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
# while not a 'q' key is pressed
while True:
    # update foot position
    my_leg.set_foot_pos(Position(my_leg.foot_pos.x + 2, -50, my_leg.foot_pos.z + 5))
    # update figure
    update_fig_leg(fig, my_leg)
    # wait for a key press
    plt.pause(0.1)
    # if a 'q' key is pressed, stop the loop
    if keyboard.is_pressed("q"):
        print("End.")
        break