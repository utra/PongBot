import math
import numpy as np
import matplotlib.pyplot as plt

# Constants
CUP_HEIGHT = 0.12 # metres
DRAG_FORCE = 0.5*1.225*math.pi*0.02**2*0.47# newtons/(metre/second)^2
G = 9.81 # metres/second^2
BALL_MASS = 0.0027 #kilograms

# Parameters we can control
height = 0.8 # metres
r_wheel = 0.03 # metres

def max_distance(init_vel):
    theta = optimal_angle(init_vel)
    print("Optimal angle", theta/math.pi*180)
    distance = init_vel*math.cos(theta)/G*(init_vel*math.sin(theta) + \
            math.sqrt(init_vel**2*math.sin(theta)**2 + 2*G*(height - CUP_HEIGHT)))
    print("Range", distance)
    rpm = init_vel/r_wheel/(2*math.pi)*60
    print("RPM:", rpm)
    flight_time = distance/(init_vel*math.cos(theta))
    print("Flight time:", flight_time, "seconds")

def optimal_angle(init_vel):
    '''
    Calculate the angle yielding the largest distance
    '''
    # Interestingly enough, this doesn't change with air resistance
    return math.acos((2*G*(height-CUP_HEIGHT) + init_vel)/(2*G*(height-CUP_HEIGHT) + 2*init_vel))

def simulate_flight(init_vel, theta, dt = 0.0001):
    '''
    Simulate the flight of the ball with air resistance
    '''
    # Initialize physical parameters
    t = 0
    xs = []
    ys = []
    pos = [0, height]
    vel = [init_vel*math.cos(theta), init_vel*math.sin(theta)]
    
    while pos[1] > CUP_HEIGHT:
        # Add position for the plot
        xs.append(pos[0])
        ys.append(pos[1])
        # Update the position
        pos[0] += vel[0]*dt
        pos[1] += vel[1]*dt
        # Increment the velocity based on the forces involved
        vel[0] -= DRAG_FORCE*vel[0]**2/BALL_MASS*dt
        if vel[1] > 0:
            # If rising, drag pulls it down
            vel[1] += (-G - DRAG_FORCE*vel[1]**2/BALL_MASS)*dt
        else:
            # If falling, drag pulls it up
            vel[1] += (-G + DRAG_FORCE*vel[1]**2/BALL_MASS)*dt
        t += dt

    print("Landed", pos[0], "metres away")
    print("Flew for", t, "seconds")
    # Plot the trajectory
    plt.plot(xs, ys)
    plt.show()

# Run simulation for theta going from 0.1 to 1 radians
for theta in range(10, 100, 5):
    theta = theta/100.
    print 'Theta:', theta
    simulate_flight(6.0, theta) 
