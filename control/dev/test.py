import time
import leg_controller
from params import *
    

# create a new Leg instance
leg = leg_controller.LegPy([120.0, 50.0, -425.0])
print(leg.to_string())

# RUN A SIMPLE TEST
while True:
    # loop from -100 to 50 with a step of 10
    for i in range(-100, 50, 10):
        leg.set_foot_position([120.0, i, -425.0])
        print(leg.to_string())
        time.sleep(0.3)
    # loop from 50 to -100 with a step of 10
    for i in range(50, 100, 10):
        leg.set_foot_position([120.0, i, -425.0])
        print(leg.to_string())
        time.sleep(0.3)