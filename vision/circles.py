''' ---Work in progress---

This is a short program that detects the circles in a given image, produces 
an image with all the circles outlined, and lists their positions and radii 
as well as listing the circle with the smallest x-position that is in the 
right half of the image (i.e. opponent's closest cup).

It requires the parameters of image name, min/max radius, and min distance 
between circles (all in pixels). It uses Hough Circle Detection as provided 
in OpenCV. It only detects perfect (or close to perfect) circles. The image 
needs to be of reasonably good quality and the cups need to be pretty 
distinguishable from the table.
'''

import cv2
import numpy as np

def findcircles(img_name, min_rad, max_rad, min_dist):
    ''' (str, int, int, int) -> (circle_data, img_with_circles)
    
    Take an image, find the circles inside it, return the image with the
    circles drawn and an array of the circle data
    '''
    
    img = cv2.imread(img_name, 0)
    img = cv2.medianBlur(img, 5) # blur img to make circles easier to detect
    
    gray = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR) 
    #create new grayscale version of image to draw circles on
    
    circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 0.1, min_dist,
                               param1=50, param2=50,
                               minRadius=min_rad, maxRadius=max_rad)
    # make an array of the circles detected in the image, finding (x, y, r
    # param2 is the threshold value)
    
    # round values to ints
    circles = np.round(circles[0, :]).astype('int') if not \
        circles == None else []
    for (x, y, r) in circles:
        cv2.circle(gray, (x, y), r, (0, 255, 0), 2) # draw outer circle
        cv2.circle(gray, (x, y), 2, (0, 0, 255), 2) # draw center of circle
    
    ans = raw_input('Show the detected circles or nah (y/n)? ')
    
    if ans == 'y':
        print 'Enter any key to close the window.'
        cv2.imshow('detected cups',gray)
        cv2.waitKey(0)
        cv2.destroyWindow('detected cups') # close window with any key        
    
    return (circles, gray)

def findclosestcircle(img_name, min_rad, max_rad, min_dist):
    ''' (str, int, int) -> None
    
    Use findcircles to find the circles in the image, return the x and y
    coordinates of the closest circle that is past the middle of the image
    '''
    
    image = findcircles(img_name, min_rad, max_rad, min_dist)
    circles = image[0]
    gray = image[1]
    
    if len(circles) == 0:
        raise Exception('No circles found.')
    
    for (x, y, r), i in zip(circles, range(1, len(circles) + 1)):
        # print out locations of circles
        print 'Circle {}: x = {}, y = {}, r = {}'.format(i, x, y, r)
    
    width = gray.shape[1] # width of image
    opp_cups = [(x, y, r) for (x, y, r) in circles if x > width/2] # opponent's cups
    closest = min(opp_cups) # minimum x-value corresponds to closest cup
    x, y, r = closest[0], closest[1], closest[2]
    print 'The closest opponent cup is at x = {}, and y = {}.'.format(x, y)
    
    show = raw_input('Outline closest circle (y/n)? ')
    if show == 'y':
        cv2.circle(gray, (x, y), r, (0,255,255), 2) # draw outer circle
        cv2.circle(gray, (x, y), 2, (255,218,185), 2) # draw center of circle
        print 'Enter any key to close the window.'
        cv2.imshow('closest cup', gray)
        cv2.waitKey(0)
        cv2.destroyWindow('closest cup') # close window with any key        

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 5:
        findclosestcircle(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
                          int(sys.argv[4]))
    else:
        name = raw_input('Enter the image name or path (incl. extension): ')
        min_rad = raw_input('Enter the minimum radius: ')
        max_rad = raw_input('Enter the maximum radius: ')
        min_dist = raw_input('Enter the minimum distance between circles: ')
        findclosestcircle(name, int(min_rad), int(max_rad), int(min_dist))
