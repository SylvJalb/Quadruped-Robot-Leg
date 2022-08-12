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
foot_pos = Position(120, 50, -400)
my_leg = Leg(foot_pos)
my_leg.calibrate_leg()


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
walk = False
push = True
foot_pos_init = Position(foot_pos.x, foot_pos.y, foot_pos.z)

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
print("Press '5' to quit")

# while not a '5' key is pressed
while True:
    # if a 'q' key is pressed, stop the loop
    if keyboard.is_pressed("5"):
        print("End.")
        break
    # if a 'w' key is pressed, start walking
    if keyboard.is_pressed("w"):
        walk = walk == False
        # save the current foot position
        foot_pos_init.x = foot_pos.x
        foot_pos_init.y = foot_pos.y
        foot_pos_init.z = foot_pos.z

    if walk:
        if push :
            # push back the foot to go forward
            foot_pos.y -= step
            # if the foot is too pushed, stop push it back
            if foot_pos.y <= foot_pos_init.y - 170:
                push = False
            elif foot_pos.y <= foot_pos_init.y - 150:
                foot_pos.z += step
        else:
            # come back the foot in the air, to the initial position
            foot_pos.y += step
            if foot_pos.y >= foot_pos_init.y:
                foot_pos.x = foot_pos_init.x
                foot_pos.y = foot_pos_init.y
                foot_pos.z = foot_pos_init.z
            elif foot_pos.y >= foot_pos_init.y - 30:
                foot_pos.z -= step * 2
            elif foot_pos.y <= foot_pos_init.y - 100:
                foot_pos.z += step
            # if the foot is at the initial position, push it back
            if foot_pos.x == foot_pos_init.x and foot_pos.y == foot_pos_init.y and foot_pos.z == foot_pos_init.z:
                push = True
        change = True
    else :
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
    # wait a little bit
    plt.pause(0.2)

exit(1)