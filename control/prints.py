from leg import *
import matplotlib.pyplot as plt

def axe_leg(leg):
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
    ax.plot([leg.shoulder_pos.x], [leg.shoulder_pos.y], [leg.shoulder_pos.z], color='gray', marker='o', markersize=10)
    ax.text(leg.shoulder_pos.x + 15, leg.shoulder_pos.y + 15, leg.shoulder_pos.z + 15, str(round(leg.shoulder_angle, 1)), color='black')
    # trace the arm point
    ax.plot([leg.arm_pos.x], [leg.arm_pos.y], [leg.arm_pos.z], color='gray', marker='o', markersize=10)
    ax.text(leg.arm_pos.x + 15, leg.arm_pos.y + 15, leg.arm_pos.z + 15, str(round(leg.arm_angle, 1)), color='black')
    # trace the forearm point
    ax.plot([leg.forearm_pos.x], [leg.forearm_pos.y], [leg.forearm_pos.z], color='gray', marker='o', markersize=10)
    ax.text(leg.forearm_pos.x + 15, leg.forearm_pos.y + 15, leg.forearm_pos.z + 15, str(round(leg.forearm_angle, 1)), color='black')
    # trace the foot point
    ax.plot([leg.foot_pos.x], [leg.foot_pos.y], [leg.foot_pos.z], color='blue', marker='o', markersize=15)
    ax.text(leg.foot_pos.x + 15, leg.foot_pos.y + 15, leg.foot_pos.z + 15, str(leg.foot_pos), color='darkblue')

    return ax

def fig_leg(leg):
    fig = plt.figure()
    fig.add_axes(axe_leg(leg))
    return fig

def update_fig_leg(fig, leg):
    fig.clear()
    fig.add_axes(axe_leg(leg))