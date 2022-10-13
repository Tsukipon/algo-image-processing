import numpy as np
import cv2 as cv
import argparse
from enum import Enum


class blur(Enum):
    linear = 'linear'
    gaussian = 'gaussian'
    radial = 'radial'
    median = 'median'
    bilateral = 'bilateral'

    def str(self):
        return self.value


cli = argparse.ArgumentParser()
cli.add_argument("-i", "--image", required=True,
                 help="image path")
cli.add_argument("-b", "--blur", type=blur, choices=list(blur), required=False,
                 help="Blur method pre-applied before Canny Edge Detection (linear, gaussian or radial)")
cli.add_argument("-k", "--kernel", required=False,
                 help="kernel level of blurring")

args = vars(cli.parse_args())

img = cv.imread(args["image"])

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

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
        blurred = cv.GaussianBlur(gray, (int(
            args["kernel"]), int(
            args["kernel"])), 0) if args["kernel"] else cv.GaussianBlur(gray, (3, 3), 0)

cv.imshow("Canny Edge Detection",blurred)
cv.waitKey()
cv.destroyAllWindows()

computed_median = np.median(blurred)
lower_treshold = (1.0 - 0.33) * computed_median
upper_treshold = int(min(255, (1.0 + 0.33) * computed_median))


automatically_edged = ~cv.Canny(blurred, lower_treshold, upper_treshold)

wide = ~cv.Canny(img, 10, 200)
tight = ~cv.Canny(img, 225, 250)


cv.imshow("Canny Edge Detection", np.hstack(
    [tight, wide, automatically_edged]))
cv.waitKey()
cv.destroyAllWindows()
