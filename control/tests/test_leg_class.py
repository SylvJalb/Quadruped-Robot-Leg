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
step = 10
change = False
# print how to move the foot
print("To move the foot, use the keyboard: (stay pressed to move)")
print("----------")
print("|+Z|+Y|  |")
print("----------")
print("|-X|  |+X|")
print("----------")
print("|-Z|-Y|  |")
print("----------")
print("\t2: -" + str(step) + " in X", end="")
print("\t8: +" + str(step) + " in X")
print("\t4: -" + str(step) + " in Y", end="")
print("\t6: +" + str(step) + " in Y")
print("\t1: -" + str(step) + " in Z", end="")
print("\t9: +" + str(step) + " in Z")

# while not a 'q' key is pressed
while True:
    # wait a little bit
    plt.pause(0.3)
    # if a 'q' key is pressed, stop the loop
    if keyboard.is_pressed("q"):
        print("End.")
        exit()
    if keyboard.is_pressed("7"):
        foot_pos.z += step
        change = True
    if keyboard.is_pressed("1"):
        foot_pos.z -= step
        change = True
    if keyboard.is_pressed("8"):
        foot_pos.y += step
        change = True
    if keyboard.is_pressed("2"):
        foot_pos.y -= step
        change = True
    if keyboard.is_pressed("4"):
        foot_pos.x -= step
        change = True
    if keyboard.is_pressed("6"):
        foot_pos.x += step
        change = True
    if change:
        # update foot position
        my_leg.set_foot_pos(foot_pos)
        # update figure
        update_fig_leg(fig, my_leg)
        change = False