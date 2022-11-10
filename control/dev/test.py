import leg_controller

# create a new Leg instance
leg = leg_controller.LegPy([120.0, 50.0, -425.0])
print(leg.to_string())

# RUN A SIMPLE TEST
# loop from -100 to 50 with a step of 10
for i in range(-100, 50, 10):
    leg.set_foot_position([120.0, i, -425.0])
    print(leg.to_string())