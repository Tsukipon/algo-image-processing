import turtle
from sklearn.neighbors import KDTree
import time
import numpy as np
import math

def getPixelCoordinatesBygroup(image,group):
    coords = []
    height = len(image)
    if isinstance(group, int):
        dim = 1
    else:
        dim = len(group)
    if dim == 1:
        for y, line in enumerate(image):
            for x, value in enumerate(line):
                if value == group:
                    coords.append([x, height - y])
    else:
        for y, line in enumerate(image):
            for x, value in enumerate(line):
                if value[0] == group[0] and value[1] == group[1] and value[2] == group[2]:
                    coords.append([x, height - y])
    return coords




def drawKDTree(pen, coords, shape):
    start = time.time()
    width = int(shape[1])
    height = int(shape[0])
    pen.penup()
    tree = KDTree(coords)
    current = 0
    explored_ind = [0]

    while len(coords) > 1 :
        pen.goto(coords[current][0] - (width/2), coords[current][1]- (height/2))
        ind= tree.query_radius([coords[current]], r=1.42)
        ind = ind[0].tolist()
        ind = [value for value in ind if value not in explored_ind]

        if len(ind) >= 1:
            pen.pendown()
            pen.goto(coords[ind[0]][0] - (width/2), coords[ind[0]][1]- (height/2))
            pen.penup()
            explored_ind.append(ind[0])
            current = ind[0]
                    
            
        else:
            tmp=coords[current]
            coords = [coords[i] for i in range(0,len(coords)) if i not in explored_ind]
            explored_ind = []
            if(len(coords) > 1):
                tree = KDTree(coords)
                dist,i = tree.query([tmp],k=2)
                i = i.flatten()
                current = i[1]
    end = time.time()
    print("execution time : ",end - start)


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



def drawBasic(pen, coords, shape,color):
    start = time.time()
    width = int(shape[1])
    height = int(shape[0])
    pen.color(color)
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


def paint(pen,coords,shape,color):
    width = int(shape[1])
    height = int(shape[0])
    pen.color(color)
    pen.penup()
    for coord in coords:
        pen.setpos(coord[0] - (width/2), coord[1]- (height/2))
        pen.dot(1)
    





def draw(new_matrix: list, window: tuple, drawing_speed: int) -> None:
    screen = turtle.Screen()
    screen.title("monetmaker")
    screen.screensize(window[0], window[1])
    screen.colormode(255)
    pen = turtle.Turtle()
    pen.ht()
    screen.tracer(drawing_speed)
    image_width = new_matrix.shape[1]
    image_height = new_matrix.shape[0]
    for y in range(int(image_height/2), int(image_height/-2),  -1):
        pen.penup()
        pen.goto(-(image_width / 2), y)
        pen.pendown()
        for x in range(-int(image_width/2), int(image_width/2), 1):
            pix_width = int(x + (image_width/2))
            pix_height = int(image_height/2 - y)
            pen.color(new_matrix[pix_height, pix_width])
            pen.forward(1)
        screen.update()
    turtle.done()
    return
