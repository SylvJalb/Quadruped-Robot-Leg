from scipy.spatial.transform import Rotation
import numpy as np

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


def rotate_around(pos, angle, axis_array):
    """
    Rotate a vector around the y axis by a given angle
    Link used : https://www.adamsmith.haus/python/answers/how-to-rotate-a-3d-vector-about-an-axis-in-python
    """
    vec = [pos.x, pos.y, pos.z]

    rotation_degrees = angle
    rotation_radians = np.radians(rotation_degrees)
    rotation_axis = np.array(axis_array) # We rotate around the y axis

    rotation_vector = rotation_radians * rotation_axis
    # Use a scipy function to rotate the vector
    rotation = Rotation.from_rotvec(rotation_vector)
    rotated_vec = rotation.apply(vec)
    pos_result = Position(rotated_vec[0], rotated_vec[1], rotated_vec[2])
    # print("###### ROTATE AROUND ######")
    # print("pos: {}".format(pos))
    # print("pos_result: {}".format(pos_result))
    # print("###########################")
    return pos_result