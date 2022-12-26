import sys
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

        self.foot_pos = [120.0, 30.0, -425.0]

        # create a new Leg instance
        self.leg = leg_controller.LegPy(self.foot_pos)
        print(self.leg.to_string())

        # set the background color
        self.setBackgroundColor(1.0, 1.0, 1.0, 1.0)
        
        # Create a point light to illuminate the scene
        plight = PointLight('plight')
        plight.setColor((1.0, 1.0, 1.0, 1.0))
        plnp = self.render.attach_new_node(plight)
        plnp.set_pos(400.0, 50.0, 300.0)
        self.render.set_light(plnp)

        # Load models.
        self.struct_obj = self.loader.load_model("models/struct.obj")
        self.shoulder_obj = self.loader.load_model("models/shoulder.obj")
        self.arm_obj = self.loader.load_model("models/arm.obj")
        self.forearm_obj = self.loader.load_model("models/forearm.obj")
        # Set diff vectors
        # rotate the model so it faces the right direction
        self.struct_obj.set_hpr(0.0, 90.0, 90.0)
        # replace origin with the center of the model
        self.struct_obj.set_pos(0.0, -200.0, -500.0)
        # Reparent the model to render.
        self.struct_obj.reparent_to(self.render)
        self.shoulder_obj.reparent_to(self.render)
        self.arm_obj.reparent_to(self.render)
        self.forearm_obj.reparent_to(self.render)
        self.update_models()

        self.accept('v', self.show_camera)
        self.accept('v-up', self.unshow_camera)
        self.accept('escape', sys.exit)
    
    def run_walk(self):
        self.walking_step = -10
        # Create a task to update the simulation
        self.taskMgr.add(self.update_walk, 'UpdateWalk', sort=1)
        self.run()

    def show_camera(self):
        self.taskMgr.add(self.update_camera, 'UpdateCamera', sort=1)
    def unshow_camera(self):
        self.taskMgr.remove('UpdateCamera')

    def update_camera(self, task):
        # Set the camera position and orientation
        self.camera.setPos(1200.0, 500.0, 350.0)
        self.camera.lookAt(0.0, -10.0, -150.0)
        
        # Return Task.cont to indicate that the task should continue running
        return task.cont

    def update_walk(self, task):
        # Update the leg
        if self.foot_pos[1] < -100:
            self.walking_step = 10
        elif self.foot_pos[1] > 100:
            self.walking_step = -10
            
        self.foot_pos[1] += self.walking_step
        self.foot_pos[2] += self.walking_step / 2
        self.leg.set_foot_position(self.foot_pos)

        # Clear the previous lines
        self.update_models()
        print(self.leg.to_string())
        print(self.arm_obj.get_hpr())

        time.sleep(0.05)

        return task.cont
    
    def update_models(self):
        # Update the models
        shoulder_pos, arm_pos, forearm_pos, foot_pos = self.get_positions_from_leg()
        shoulder_angle, arm_angle, forearm_angle = self.get_angles_from_leg()
        self.shoulder_obj.set_pos(shoulder_pos)
        self.shoulder_obj.set_hpr(-90.0, shoulder_angle, 0.0)
        self.arm_obj.set_pos(arm_pos)
        self.arm_obj.set_hpr(-90.0, shoulder_angle, -arm_angle)
        self.forearm_obj.set_pos(forearm_pos)
        self.forearm_obj.set_hpr(-90.0, shoulder_angle, -(arm_angle + forearm_angle))
        
    
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