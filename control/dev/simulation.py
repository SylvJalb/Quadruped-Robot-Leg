from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, CardMaker, PointLight, loadPrcFile, BoundingSphere, NodePath

import leg_controller
from params import *

import time

class SimulationApp(ShowBase):
    def __init__(self):
        loadPrcFile("simu_config.prc")
        # Initialize the ShowBase class
        ShowBase.__init__(self)

        self.foot_pos = [120.0, 50.0, -425.0]

        # create a new Leg instance
        self.leg = leg_controller.LegPy(self.foot_pos)
        print(self.leg.to_string())
        
        # Create a point light to illuminate the scene
        plight = PointLight('plight')
        plight.setColor((1.0, 1.0, 1.0, 1.0))
        plnp = self.render.attach_new_node(plight)
        plnp.set_pos(50.0, 250.0, 250.0)
        self.render.set_light(plnp)

        self.draw_leg()

        # Create a task to update the simulation
        self.taskMgr.add(self.update_camera, "UpdateCamera")
        self.taskMgr.add(self.update_leg_pos, 'update_leg_pos')

    def update_camera(self, task):
        
        # Set the camera position and orientation
        self.camera.setPos(800.0, 100.0, 350.0)
        self.camera.lookAt(0.0, -10.0, -230.0)
        
        # Return Task.cont to indicate that the task should continue running
        return task.cont

    def update_leg_pos(self, task):
        # Update the leg
        if self.foot_pos[1] < -100:
            self.foot_pos[1] = 100
        else:
            self.foot_pos[1] -= 10
        self.leg.set_foot_position(self.foot_pos)

        # Clear the previous lines
        self.draw_leg()

        return task.cont
    
    def draw_leg(self):
        print(self.leg.to_string())
        # Get the positions of the main points of the leg
        shoulder_pos, arm_pos, forearm_pos, foot_pos = self.get_positions_from_leg()
        # Get the angles of the main points of the leg
        # shoulder_angle, arm_angle, forearm_angle = self.get_angles_from_leg(leg)

        # Create a LineSegs object to hold the lines representing the bones
        line_segs = LineSegs()
        line_segs.set_thickness(10.0)
        line_segs.set_color(*(1.0, 0.0, 0.0, 1.0)) # red

        # Create a line for each bone
        line_segs.move_to(shoulder_pos)
        line_segs.draw_to(arm_pos)
        line_segs.set_color(*(0.0, 0.0, 1.0, 1.0)) # blue
        line_segs.move_to(arm_pos)
        line_segs.draw_to(forearm_pos)
        line_segs.set_color(*(0.0, 1.0, 0.0, 1.0)) # green
        line_segs.move_to(forearm_pos)
        line_segs.draw_to(foot_pos)

        # Create a node to hold the lines and attach it to the render tree
        line_node = line_segs.create()
        self.render.attach_new_node(line_node)
    
    # Return the main points positions of the leg
    # in the form of a tuple
    # in the order: shoulder, arm, forearm, foot
    def get_positions_from_leg(self):
        shoulder_pos = tuple(self.leg.get_shoulder_position())
        arm_pos = tuple(self.leg.get_arm_position())
        forearm_pos = tuple(self.leg.get_forearm_position())
        foot_pos = tuple(self.leg.get_foot_position())
        return shoulder_pos, arm_pos, forearm_pos, foot_pos
    
    # Return the main points angles of the leg
    # in the form of a tuple
    # in the order: shoulder, arm, forearm
    def get_angles_from_leg(self):
        shoulder_angle = self.leg.get_shoulder_angle()
        arm_angle = self.leg.get_arm_angle()
        forearm_angle = self.leg.get_forearm_angle()
        return shoulder_angle, arm_angle, forearm_angle