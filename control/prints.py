from leg import *
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

def fig_leg(leg):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim3d(X_MIN, X_MAX)
    ax.set_ylim3d(Y_MIN, Y_MAX)
    ax.set_zlim3d(Z_MIN, Z_MAX)
    ax.plot([leg.shoulder_pos.x, leg.arm_pos.x, leg.forearm_pos.x, leg.foot_pos.x],
            [leg.shoulder_pos.y, leg.arm_pos.y, leg.forearm_pos.y, leg.foot_pos.y],
            [leg.shoulder_pos.z, leg.arm_pos.z, leg.forearm_pos.z, leg.foot_pos.z],
            color='red', linewidth=3)
    # trace the shoulder point
    ax.plot([leg.shoulder_pos.x], [leg.shoulder_pos.y], [leg.shoulder_pos.z], color='black', marker='o', markersize=10)
    # trace the arm point
    ax.plot([leg.arm_pos.x], [leg.arm_pos.y], [leg.arm_pos.z], color='black', marker='o', markersize=10)
    # trace the forearm point
    ax.plot([leg.forearm_pos.x], [leg.forearm_pos.y], [leg.forearm_pos.z], color='black', marker='o', markersize=10)
    # trace the foot point
    ax.plot([leg.foot_pos.x], [leg.foot_pos.y], [leg.foot_pos.z], color='blue', marker='o', markersize=15)
    return fig
