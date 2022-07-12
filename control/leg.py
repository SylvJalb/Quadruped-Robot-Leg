import numpy as np
from math import sqrt, acos, atan2, sin, cos
from scipy.spatial.transform import Rotation

from numpy import arccos
from params import *

class Position:
    """
    Position of the leg
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "x={}, y={}, z={}".format(self.x, self.y, self.z)

# Leg class
class Leg:
    def __init__(self, foot_position):
        """
        Initialize the leg
        footPos : position of foot
        """
        self.foot_pos = foot_position
        self.shoulder_pos = Position(0, 0, 0)
        self.arm_pos = self.calcul_arm_position()
        self.shoulder_angle = self.calcul_shoulder_angle()
        self.forearm_pos = self.calcul_forearm_position()
        self.arm_angle = self.calcul_arm_angle()
        self.forearm_angle = self.calcul_forearm_angle()
    
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
        return acos(adj / hyp)
    
    def calcul_forearm_position(self):
        """
        Calculates the Forearm position from the foot position and the arm position
        APF points : A->Arm, P->Foot, F->Forearm
        Work in 3D space (x, y, z)
        How it's working :
             1) To simplify the calculations we simulate a rotation of shoulder to have the arm verticaly.
                And, covert to 2D the y and z coordinates of the arm -> (temporarily renamed 'x' and 'y')
             2) We calculate intersections between the circle around A and around P.
             3) Get the intersection have the lowest x value.
             4) Reconvert the intersection result to the 3D space. And reverse rotation.
        """
        # Parameters for the calculations
        P = Position(self.foot_pos.x, self.foot_pos.y, self.foot_pos.z)
        A = Position(self.arm_pos.x, self.arm_pos.y, self.arm_pos.z)
        PR = FOREARM_LENGTH # radius of the Foot circle
        AR = ARM_LENGTH # radius of the Arm circle

        # 1) To simplify the calculations we simulate a rotation of shoulder to have the arm verticaly.
        def rotate_around_y(pos, angle):
            """
            Rotate a vector around the y axis by a given angle
            Link used : https://www.adamsmith.haus/python/answers/how-to-rotate-a-3d-vector-about-an-axis-in-python
            """
            vec = [pos.x, pos.y, pos.z]

            rotation_degrees = angle
            rotation_radians = np.radians(rotation_degrees)
            rotation_axis = np.array([0, 1, 0]) # We rotate around the y axis

            rotation_vector = rotation_radians * rotation_axis
            # Use a scipy function to rotate the vector
            rotation = Rotation.from_rotvec(rotation_vector)
            rotated_vec = rotation.apply(vec)
            pos_result = Position(rotated_vec[0], rotated_vec[1], rotated_vec[2])
            # print("######")
            # print(pos)
            # print(pos_result)
            # print("######")
            return pos_result
        
        # Do the rotation
        AC = rotate_around_y(A, -self.shoulder_angle)
        PC = rotate_around_y(P, -self.shoulder_angle)
        # Convert to 2D
        PC_2D = Position(PC.y, PC.z, 0)
        AC_2D = Position(AC.y, AC.z, 0)

        # check if the conversion is correct
        print("AC_2D is normaly (0,0,0) :")
        print("\tcheck -> {coord}".format(coord = str(AC_2D)))

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
        F = rotate_around_y(FC, self.shoulder_angle)

        return F
    
    def calcul_arm_angle(self):
        """
        Calculates the Arm angle from the arm position and forearm position
        """
        # TODO
        return 0
    
    def calcul_forearm_angle(self):
        """
        Calculates the Forearm angle from the forearm position
        """
        # TODO
        return 0
    
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
            self.arm_pos = self.calcul_arm_position()
            self.shoulder_angle = self.calcul_shoulder_angle()
            self.forearm_pos = self.calcul_forearm_position()
            self.arm_angle = self.calcul_arm_angle()
            self.forearm_angle = self.calcul_forearm_angle()
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