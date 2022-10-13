import argparse
from enum import Enum
import cv2 as cv

from classification import classify_pixels
from clustering import cluster_pixels
from draw import draw,drawKDTree,getPixelCoordinatesBygroup , drawBasic,paint
import turtle
import numpy as np



WIDTH, HEIGHT = 800, 800
window_size = []
COLOR_PALETTE = {0: (112, 78, 46), 1: (121, 116, 46),
                 2: (194, 231, 127), 3: (230, 248, 178),
                 4: (112, 145, 118)}


class blur(Enum):
    linear = 'linear'
    gaussian = 'gaussian'
    radial = 'radial'
    median = 'median'
    bilateral = 'bilateral'
    def str(self):
        return self.value


class algorithm(Enum):
    clustering = 'clustering'
    classification = 'classification'
    def str(self):
        return self.value


cli = argparse.ArgumentParser()
cli.add_argument("-i", "--image", required=True,
                 help="image path")
cli.add_argument("-b", "--blur", type=blur, choices=list(blur), required=False,
                 help="blur method pre-applied before Canny Edge Detection (linear, gaussian or radial)")
cli.add_argument("-k", "--kernel", required=False,
                 help="kernel level of blurring")
cli.add_argument("-W", "--width", required=False,
                 help="window width")
cli.add_argument("-H", "--height", required=False,
                 help="window height")
cli.add_argument("-s", "--speed", required=False,
                 help="drawing speed in pixels")
cli.add_argument("-a", "--algorithm", required=False,
                 help="clustering or classification")
cli.add_argument("-p", "--painting", required=False,
                 help="normal or realistic")


args = vars(cli.parse_args())

img = cv.imread(args["image"])

# noise reduction
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


# Apply Blur method
if "blur" in args:
    if args["blur"] == "linear":
        blurred = cv.boxFilter(gray, -1, int(args["kernel"]), normalize=False,
                               ) if args["kernel"] else cv.boxFilter(gray, -1, 3, normalize=False)
    elif args["blur"] == "median":
        blurred = cv.medianBlur(
            gray, int(args["kernel"])) if args["kernel"] else cv.medianBlur(gray, 3)
    elif args["blur"] == "bilateral":
        blurred = cv.bilateralFilter(gray, int(
            args["kernel"]), 75, 75) if args["kernel"] else cv.medianBlur(gray, 9, 75, 75)
    else:
        # gaussian blur by default
        blurred = cv.GaussianBlur(gray, (int(
            args["kernel"]), int(
            args["kernel"])), 0) if args["kernel"] else cv.GaussianBlur(gray, (3, 3), 0)

if "speed" in args and args["speed"]:
    drawing_speed = int(args["speed"])
else:
    drawing_speed = 0

if "width" in args and "height" in args and args["width"] and args["height"]:
    window_size = (int(args["width"]), int(args["height"]))
else:
    window_size.append(WIDTH)
    window_size.append(HEIGHT)

computed_median = np.median(blurred)
# apply automatic Canny edge detection using the computed median
lower_treshold = (1.0 - 0.33) * computed_median
# Here we consider that the max value the image is 255 ( 8bit images)
upper_treshold = int(min(255, (1.0 + 0.33) * computed_median))
automatically_edged = ~cv.Canny(blurred, lower_treshold, upper_treshold)

#dst contain the resulting binary image.
retval, dst = cv.threshold(automatically_edged, 127, 255, cv.THRESH_BINARY)

coords = getPixelCoordinatesBygroup(dst,0)

screen = turtle.Screen()
screen.title("monetmaker")
screen.screensize(window_size[0], window_size[1])

pen = turtle.Turtle()
pen.speed(drawing_speed)
screen.tracer(drawing_speed, 0)
pen.ht()

drawBasic(pen,coords,blurred.shape,(0,0,0))

screen.colormode(255)
if "algorithm" in args and args["algorithm"] == "classification":
    new_matrix = classify_pixels(img, COLOR_PALETTE)
    for value in COLOR_PALETTE.values():
        print("Painting color: ",value)
        coords = getPixelCoordinatesBygroup(new_matrix,value)

        if "painting" in args and args["painting"] == "realistic":
            drawBasic(pen, coords, new_matrix.shape,value)
        else:
            paint(pen, coords, new_matrix.shape,value)
    
else:
    
    x, y, data_size = img.shape
    #new_matrix = cluster_pixels(img)
    kmeans = cluster_pixels(img)
    mapping = kmeans.labels_.reshape((x,y))
    ngroup = len(kmeans.cluster_centers_)

    if "painting" in args and args["painting"] == "realistic":
        for i in range(0,ngroup):
            color = kmeans.cluster_centers_[i]
            colorInt=((int(color[0]),int(color[1]),int(color[2])))
            print("Painting color: ",colorInt)
            coords = getPixelCoordinatesBygroup(mapping,i)
            drawBasic(pen, coords, img.shape,colorInt)
    else:
        for i in range(0,ngroup):
            color = kmeans.cluster_centers_[i]
            colorInt=((int(color[0]),int(color[1]),int(color[2])))
            print("Painting color: ",colorInt)
            coords = getPixelCoordinatesBygroup(mapping,i)
            paint(pen, coords, img.shape,colorInt)



turtle.done()
print('Finished drawing')
