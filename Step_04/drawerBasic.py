import cv2 as cv
import math
import numpy as np
import time

#For binary images black pixel has a value of 0
def getPixelCoordinates(image):
    coords = []
    height = len(image)
    for y, line in enumerate(image):
        for x, value in enumerate(line):
            if value == 0:
                coords.append([x, height - y])
    return coords


#coord must not be included in coords
#return position of closest pixel
def getClosestFriend(coord,coords):
    minimum = np.Infinity
    for i,val in enumerate(coords):
        dist = math.dist(coord,val)
        if dist< 1.42:
            return coords.pop(i)
        if dist < minimum:
            minimum = dist
            closest = i
    return coords.pop(closest)



def draw(pen, coords, shape):
    start = time.time()
    width = int(shape[1])
    height = int(shape[0])
    pen.penup()

    current = coords.pop(0)
    pen.goto(current[0] - (width/2), current[1]- (height/2))

    while coords:
        closest = getClosestFriend(current,coords)
        dist = math.dist(current,closest)
        if dist <1.42:
            pen.pendown()
            pen.goto(closest[0] - (width/2), closest[1]- (height/2))
            pen.penup()
            current=closest
        else:
            current = closest
            pen.goto(current[0] - (width/2), current[1]- (height/2))
    end = time.time()
    print("execution time : ",end - start)



                    







#
#def draw(pen, coords, shape):
#
#    width = int(shape[1])
#    height = int(shape[0])
#
#    pen.penup()
#    current_i = 0
#    for i in range (0, len(coords)):
#        tree = KDTree(coords, 1)
#
#        current = coords[current_i]
#        x = coords[current_i][0]
#        y = coords[current_i][1]
#        pen.goto(x - (width/2), y - (height/2))
#
#        distance, indexes = tree.query([coords[current_i]], 2) # maybe add distance
#        neighbour_i = indexes[0][1]
#        neighbour = coords[neighbour_i]
#
#        distance = math.dist([x, y], [neighbour[0],  neighbour[1]])
#        if (distance <= 2.):
#          pen.pendown()
#          pen.goto(neighbour[0] - (width/2), neighbour[1]- (height/2))
#          pen.penup()
#
#        coords[current_i] = [0, 0]
#        current_i = neighbour_i
#
#    # Hotfix, TODO, understand why some coordinates are not taken in account
#    coords_left = list(filter(lambda x: x != [0, 0], coords))
#    if len(coords) > 0:
#        draw(pen, coords_left, shape)
#
#