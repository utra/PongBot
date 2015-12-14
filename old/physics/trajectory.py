'''
This program computes the firing angle above the horizontal needed to hit
a target a given distance away, subject to the constraint of firing speed.
'''

import math
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import sys

# Constants
CUP_HEIGHT = 0.12 # metres
DRAG_FORCE = 0.5*1.225*math.pi*0.02**2*0.47# newtons/(metre/second)^2
G = 9.81 # metres/second^2
BALL_MASS = 0.0027 #kilograms

# Parameters we can control
height = 0.350 # metres
r_wheel = 0.03 # metres
epsilon = 0.001 # metres, millimeter accuracy

def max_distance(init_vel):
    theta = optimal_angle(init_vel)
    print("Optimal angle:", theta/math.pi*180, "degrees")
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
    optimal_angle = math.acos(math.sqrt((2*G*(height-CUP_HEIGHT) + init_vel**2)/(2*G*(height-CUP_HEIGHT) + 2*init_vel**2)))
    print 'Optimal angle:', optimal_angle/math.pi*180, "degrees"
    return optimal_angle

def simulate_flight(init_vel, theta, dt = 0.0001, verbose=False):
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

    if verbose:
        # Print out details of flight and show plot
        print 'Printing verbose trajectory output'
        print 'Flight time:', t, 'seconds'
        print 'Max height:', max(ys), 'metres'
        print 'Distance:', xs[-1], 'metres'
        plt.plot(xs, ys)
        plt.xlabel('Distance (m)')
        plt.ylabel('Height (m)')
        plt.show()

    return xs[-1]

def get_angle(distance, v_max):
    '''
    For a given distance, find the angle required to shoot there
    shooting at the highest velocity. Uses successive bisection 
    and simulation, since inverting the distance function is hard
    with air drag in the mix.
    '''

    theta_min = optimal_angle(v_max)
    theta_max = 1.5 # radians
    theta = theta_max
    projected_distance = -1000 # dummy value

    # Shooting too far
    if (simulate_flight(v_max, theta_min) < distance):
        print "Sorry, can't shoot that far for that v_max"
        return -1

    # Loop, bisecting, until the distance converges
    while (abs(projected_distance - distance) > epsilon):
        projected_distance_min = simulate_flight(v_max, theta_min)
        projected_distance_max = simulate_flight(v_max, theta_max)
        # Make sure we can bisect, distance falls in between
        if (projected_distance_min > distance > projected_distance_max):
            if abs(projected_distance_min - distance) < \
                abs(projected_distance_max - distance):
                # Theta min gets you closer
                projected_distance = projected_distance_min
                theta = theta_min
                theta_max = (theta_min + theta_max)/2.
            else:
                # Theta max gets you closer
                projected_distance = projected_distance_max
                theta = theta_max
                theta_min = (theta_min + theta_max)/2.
        # If we can't bisect, change the bounds
        else:
            if (projected_distance_min < distance):
                theta_min -= 0.01
            elif (projected_distance_max > distance):
                theta_max += 0.01

    return theta

if __name__ == "__main__":
    if (len(sys.argv) == 3):
        distance = float(sys.argv[1])
        v_max = float(sys.argv[2])

        def simulate(theta):
            return -simulate_flight(v_max, theta)

        print minimize(simulate, 0.5)

        print 'Distance:', distance, 'metres'
        print 'Maximum velocity:', v_max, 'metres/second'
        # Run simulation for theta going from 0.1 to 1 radians
        theta = get_angle(distance, v_max)
        if theta != -1:
            print 'Firing angle:', theta/math.pi*180, 'degrees above the horizontal'
            simulate_flight(v_max, theta, verbose=False)
    else: 
        print 'To run the program, enter "python trajectory.py <distance> <v_max>"'

