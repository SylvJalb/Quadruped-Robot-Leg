from math import degrees, sqrt, acos, atan2, sin, cos
from time import sleep


from numpy import arccos
from params import *
from geometry import *

from setup import *
from env import *

# Leg class
class Leg:
    def __init__(self, foot_position):
        """
        Initialize the leg
        footPos : position of foot
        """
        self.foot_pos = foot_position
        self.odrives_ready = False
        self.update_leg_positions()

        try:
            print("Searching for ODrives cards...")
            self.oDrive1, self.oDrive2 = find_odrives()

            self.shoulder = self.oDrive1.axis0
            self.arm = self.oDrive2.axis1
            self.forearm = self.oDrive2.axis0
            print("ODrives cards found")
            print("Setup ODrives cards...")
            setup_odrive(self.shoulder)
            setup_odrive(self.arm)
            setup_odrive(self.forearm)
            print("ODrives cards configured")
            self.odrives_ready = True
        except:
            self.odrives_ready = False
            print("No ODrives cards found")
    
    def calibrate_leg(self):
        """
        Calibrate the leg
        """
        if self.odrives_ready:
            print("Calibrating :")
            print("\tshoulder...", end="")
            run_calibration(self.shoulder)
            print("\tarm...", end="")
            run_calibration(self.arm)
            print("\tforearm...\n")
            run_calibration(self.forearm)
            # wait for the end of the calibration
            while not self.shoulder.motor.is_calibrated or not self.arm.motor.is_calibrated or not self.forearm.motor.is_calibrated:
                sleep(0.3)
            blocked_motor_mode(self.shoulder)
            blocked_motor_mode(self.arm)
            blocked_motor_mode(self.forearm)
            print("Calibration finished")
        else:
            print("ODrives not Ready")
            
    
    def update_leg_positions(self):
        """
        Update all leg positions
        """
        self.shoulder_pos = Position(0, 0, 0)
        self.arm_pos = self.calcul_arm_position()
        self.shoulder_angle = self.calcul_shoulder_angle()
        
        # To simplify the next calculations we simulate a rotation of shoulder to have the arm verticaly.
        self.arm_vertical_pos = rotate_around(self.arm_pos, self.shoulder_angle, [0, 1, 0])
        self.foot_vertical_pos = rotate_around(self.foot_pos, self.shoulder_angle, [0, 1, 0])

        self.forearm_pos, self.forearm_vertical_pos = self.calcul_forearm_position()
        self.arm_angle = self.calcul_arm_angle()
        self.forearm_angle = self.calcul_forearm_angle()

        if self.odrives_ready:
            # Update the motors positions
            self.shoulder.controller.input_pos = self.shoulder_angle / 360 / REDUCTION_COEF
            self.arm.controller.input_pos = self.arm_angle / 360 / REDUCTION_COEF
            self.forearm.controller.input_pos = self.forearm_angle / 360 / REDUCTION_COEF
    
    def calcul_arm_position(self):
        """
        Calculates the Arm position from the foot position
        Link used : https://stackoverflow.com/a/49987361
        """
        # Parameters for the calculations
        (Px, Py) = (self.foot_pos.x, self.foot_pos.z) # Rotate axes just to simplify calculations
        (Cx, Cy) = (self.shoulder_pos.x, self.shoulder_pos.z)
        a = SHOULDER_LENGTH # radius of the circle

        b = sqrt((Px - Cx)**2 + (Py - Cy)**2)  # hypot() also works here
        th = acos(a / b)  # angle theta
        d = atan2(Py - Cy, Px - Cx)  # direction angle of point P from C
        d1 = d + th  # direction angle of point T1 from C
        d2 = d - th  # direction angle of point T2 from C

        T1x = Cx + a * cos(d1)
        T1y = Cy + a * sin(d1)
        T2x = Cx + a * cos(d2)
        T2y = Cy + a * sin(d2)

        result = Position(T1x, 0, T1y) # Virtual rotation of axes to fit the result with general coordinates

        # take the bigest x value as the arm position
        if T1x < T2x:
            result = Position(T2x, 0, T2y)
        
        return result 
    
    def calcul_shoulder_angle(self):
        """
        Calculates the Shoulder angle from the arm position
        Use SOHCAHTOA method
        """
        adj = self.arm_pos.x - self.shoulder_pos.x
        hyp = SHOULDER_LENGTH
        # Calculate the angle : cos(angle) = adj / hyp => angle = acos(adj / hyp)
        return degrees(acos(adj / hyp))
    
    def calcul_forearm_position(self):
        """
        Calculates the Forearm position from the foot position and the arm position
        APF points : A->Arm, P->Foot, F->Forearm
        Work in 3D space (x, y, z)
        How it's working :
             1) Covert to 2D the y and z coordinates of the vertical arm -> (temporarily renamed 'x' and 'y')
             2) We calculate intersections between the circle around A and around P.
             3) Get the intersection have the lowest x value.
             4) Reconvert the intersection result to the 3D space. And reverse rotation.
        """
        # Parameters for the calculations
        P = Position(self.foot_pos.x, self.foot_pos.y, self.foot_pos.z)
        A = Position(self.arm_pos.x, self.arm_pos.y, self.arm_pos.z)
        PC = self.foot_vertical_pos
        AC = self.arm_vertical_pos
        PR = FOREARM_LENGTH # radius of the Foot circle
        AR = ARM_LENGTH # radius of the Arm circle

        # 1) Convert to "2D"
        PC_2D = Position(PC.y, PC.z, 0)
        AC_2D = Position(AC.y, AC.z, 0)

        # 2) We calculate intersections between the circle around A and around P.
        delta=sqrt((AC_2D.x-PC_2D.x)**2 + (AC_2D.y-PC_2D.y)**2)
        # non intersecting
        if delta > PR + AR :
            print("No intersection")
        # One circle within other
        if delta < abs(PR-AR):
            print("No intersection")
        # coincident circles
        if delta == 0 and PR == AR:
            print("No intersection")
        
        a = (PR**2 - AR**2 + delta**2) / (2*delta)
        h = sqrt(PR**2-a**2)
        x2 = PC_2D.x+a*(AC_2D.x-PC_2D.x) / delta
        y2 = PC_2D.y+a*(AC_2D.y-PC_2D.y) / delta
        x3 = x2 + h*(AC_2D.y-PC_2D.y) / delta
        y3 = y2 - h*(AC_2D.x-PC_2D.x) / delta
        x4 = x2 - h*(AC_2D.y-PC_2D.y) / delta
        y4 = y2 + h*(AC_2D.x-PC_2D.x) / delta
        # 3) Get the intersection have the lowest x value.
        FC_2D = Position(x4, y4, 0)
        if x3 < x4:
            FC_2D = Position(x3, y3, 0)
        
        # 4) Reconvert the intersection result to the 3D space.
        FC = Position(SHOULDER_LENGTH, FC_2D.x, FC_2D.y) # add SHOULDER_LENGTH deep to the x axis
        # Reverse the rotation
        F = rotate_around(FC, -self.shoulder_angle, [0, 1, 0])

        return F, FC
    
    def calcul_arm_angle(self):
        """
        Calculates the Arm angle from the arm position and forearm position
        Use SOHCAHTOA method
        """
        adj = self.arm_vertical_pos.z - self.forearm_vertical_pos.z
        hyp = FOREARM_LENGTH
        # Calculate the angle : cos(angle) = adj / hyp => angle = acos(adj / hyp)
        return degrees(acos(adj / hyp))
    
    def calcul_forearm_angle(self):
        """
        Calculates the Forearm angle from the forearm position
        """
        a = [self.arm_vertical_pos.y, self.arm_vertical_pos.z]
        b = [self.forearm_vertical_pos.y, self.forearm_vertical_pos.z]
        c = [self.foot_vertical_pos.y, self.foot_vertical_pos.z]
        ang = degrees(atan2(c[1]-b[1], c[0]-b[0]) - atan2(a[1]-b[1], a[0]-b[0]))
        return ang
    
    def set_foot_pos(self, foot_position):
        """
        Set the foot position, and update all leg properties
        foot_position : New position of the foot
        return True if the position is valid, False otherwise
        """
        # Save state of the leg
        foot_pos_temp = self.foot_pos
        arm_pos_temp = self.arm_pos
        forearm_pos_temp = self.forearm_pos
        shoulder_angle_temp = self.shoulder_angle
        arm_angle_temp = self.arm_angle
        forearm_angle_temp = self.forearm_angle

        # Update the foot position
        self.foot_pos = foot_position
        # Try to do all the calculations
        try:
            # Update all leg properties with the result of the calculations
            self.update_leg_positions()
        except:
            # If the calculations failed, restore the previous state
            print("Error while setting foot position")
            print("Restoring previous state")
            self.foot_pos = foot_pos_temp
            self.arm_pos = arm_pos_temp
            self.forearm_pos = forearm_pos_temp
            self.shoulder_angle = shoulder_angle_temp
            self.arm_angle = arm_angle_temp
            self.forearm_angle = forearm_angle_temp
            return False
        return True