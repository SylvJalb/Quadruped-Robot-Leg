import matplotlib.pyplot as plt
from params import *

def add_axe_leg(ax, leg):
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim3d(LEG_X_MIN, LEG_X_MAX)
    ax.set_ylim3d(LEG_Y_MIN, LEG_Y_MAX)
    ax.set_zlim3d(LEG_Z_MIN, LEG_Z_MAX)
    shoulder_pos = leg.get_shoulder_position()
    arm_pos = leg.get_arm_position()
    forearm_pos = leg.get_forearm_position()
    foot_pos = leg.get_foot_position()
    shoulder_angle = leg.get_shoulder_angle()
    arm_angle = leg.get_arm_angle()
    forearm_angle = leg.get_forearm_angle()
    # trace the leg lines
    ax.plot([shoulder_pos[0], arm_pos[0], forearm_pos[0], foot_pos[0]],
            [shoulder_pos[1], arm_pos[1], forearm_pos[1], foot_pos[1]],
            [shoulder_pos[2], arm_pos[2], forearm_pos[2], foot_pos[2]],
            color='red', linewidth=3)
    # trace the shoulder point
    ax.plot([shoulder_pos[0]], [shoulder_pos[1]], [shoulder_pos[2]], color='gray', marker='o', markersize=10)
    ax.text(shoulder_pos[0] + 15, shoulder_pos[1] + 15, shoulder_pos[2] + 15, str(round(shoulder_angle, 1)), color='black')
    # trace the arm point
    ax.plot([arm_pos[0]], [arm_pos[1]], [arm_pos[2]], color='gray', marker='o', markersize=10)
    ax.text(arm_pos[0] + 15, arm_pos[1] + 15, arm_pos[2] + 15, str(round(arm_angle, 1)), color='black')
    # trace the forearm point
    ax.plot([forearm_pos[0]], [forearm_pos[1]], [forearm_pos[2]], color='gray', marker='o', markersize=10)
    ax.text(forearm_pos[0] + 15, forearm_pos[1] + 15, forearm_pos[2] + 15, str(round(forearm_angle, 1)), color='black')
    # trace the foot point
    ax.plot([foot_pos[0]], [foot_pos[1]], [foot_pos[2]], color='blue', marker='o', markersize=15)
    ax.text(foot_pos[0] + 15, foot_pos[1] + 15, foot_pos[2] + 15, str(foot_pos), color='darkblue')

def fig_leg(leg):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    add_axe_leg(ax, leg)
    return fig

def update_fig_leg(fig, leg):
    ax = fig.axes[0]
    ax.clear()
    add_axe_leg(ax, leg)