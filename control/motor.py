from params import *

def go_to_position(axis, deg):
    """
    Go to a position in deg.
    """
    print("Go to position: {}°".format(deg))
    axis.controller.input_pos = deg / 360 / REDUCTION_COEF