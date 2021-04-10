import cv2
import numpy as np


def nothing(_):
    pass


image = cv2.imread('photos/009.jpg')
image = cv2.resize(image, dsize=None, fx=0.15, fy=0.15)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

kernel = np.ones((3, 3), np.uint8)

# pomaranczowe
orange_gummies = cv2.inRange(image_hsv, (0, 130, 0), (18, 218, 255))
orange_gummies = cv2.morphologyEx(orange_gummies, cv2.MORPH_OPEN, kernel)
orange_gummies = cv2.morphologyEx(orange_gummies, cv2.MORPH_CLOSE, kernel)

cv2.imshow('fjfdi', orange_gummies)

'''
image = cv2.imread('photos/007.jpg')
image= cv2.resize(image, dsize=None, fx=0.15, fy=0.15)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

thresholded = cv2.inRange(image_hsv, (33, 29, 0), (54, 255, 255))

structuring_elem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, structuring_elem, iterations=3)

contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
'''

cv2.namedWindow('image')
cv2.createTrackbar('param1', 'image', 2, 1000, nothing)
cv2.createTrackbar('param2', 'image', 11, 30, nothing)
cv2.createTrackbar('min_dist', 'image', 10, 30, nothing)
cv2.createTrackbar('min_radius', 'image', 2, 100, nothing)
cv2.createTrackbar('max_radius', 'image', 38, 100, nothing)

while True:
    image_copy = image.copy()
    orange_gummies_copy = orange_gummies.copy()

    param1 = cv2.getTrackbarPos('param1', 'image')
    param2 = cv2.getTrackbarPos('param2', 'image')
    min_dist = cv2.getTrackbarPos('min_dist', 'image')
    min_radius = cv2.getTrackbarPos('min_radius', 'image')
    max_radius = cv2.getTrackbarPos('max_radius', 'image')

    circles = cv2.HoughCircles(orange_gummies, cv2.HOUGH_GRADIENT, 1, min_dist, param1=param1 + 1, param2=param2 + 1, minRadius=min_radius, maxRadius=max_radius)

    orange_gummies_copy = cv2.cvtColor(orange_gummies, cv2.COLOR_GRAY2BGR)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(orange_gummies_copy, (i[0], i[1]), i[2], (0, 255, 0), 2)

    cv2.imshow('image', image_copy)
    cv2.imshow('fjfdi', orange_gummies_copy)
    cv2.waitKey(100)
