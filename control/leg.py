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
        self.forearm_pos = self.calcul_forearm_position()
        self.shoulder_angle = self.calcul_shoulder_angle()
        self.arm_angle = self.calcul_arm_angle()
        self.forearm_angle = self.calcul_forearm_angle()
    
    def calcul_arm_position(self):
        """
        Calculates the Arm position from the foot position
        """
        # TODO
        return self.arm_pos
    
    def calcul_forearm_position(self):
        """
        Calculates the Forearm position from the foot position and the arm position
        """
        # TODO
        return self.forearm_pos
    
    def calcul_shoulder_angle(self):
        """
        Calculates the Shoulder angle from the arm position
        """
        # TODO
        return self.shoulder_angle
    
    def calcul_arm_angle(self):
        """
        Calculates the Arm angle from the arm position and forearm position
        """
        # TODO
        return self.arm_angle
    
    def calcul_forearm_angle(self):
        """
        Calculates the Forearm angle from the forearm position
        """
        # TODO
        return self.forearm_angle
    
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
            self.forearm_pos = self.calcul_forearm_position()
            self.shoulder_angle = self.calcul_shoulder_angle()
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