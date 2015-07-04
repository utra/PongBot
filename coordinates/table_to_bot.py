'''
Program to convert from table coordinates to coordinates w.r.t. the bot
'''

import math, sys

TABLE_LENGTH = 2.74 #metres
TABLE_WIDTH = 1.525 #metres

# Distance from bot to table
BOT_OFFSET = 0.2 #metres
BOT_POSITION = (-BOT_OFFSET, TABLE_WIDTH/2)

def get_polar_coordinates(cup_position, bot_position):
    """
    Returns the position of the cup relative to the bot
    """

    distance_x = cup_position[0] - bot_position[0]
    distance_y = cup_position[1] - bot_position[1]

    r = math.hypot(distance_x, distance_y)
    theta = math.degrees(math.atan(distance_y/distance_x))

    return r, theta

if __name__ == '__main__':
    if len(sys.argv) == 3:
        cup_x = sys.argv[1]
        cup_y = sys.argv[2]
    
    else:
        cup_x = raw_input("Enter the cup's x coordinate (m): ")
        cup_y = raw_input("Enter the cup's y coordinate (m): ")

    cup_position = (float(cup_x), float(cup_y))
    r, theta = get_polar_coordinates(cup_position, BOT_POSITION)

    print "Distance to cup (m):", r, "metres"
    print "Angle to cup:", theta, "degrees"
