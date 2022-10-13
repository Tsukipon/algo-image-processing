from sklearn.neighbors import KDTree
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

def draw(pen, coords, shape):
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
   
        

