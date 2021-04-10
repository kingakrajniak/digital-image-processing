# algorithm for establishing parameters for detecting gummies of one colour

import cv2


def nothing():
    pass


def main():
    image = cv2.imread('photos/009.jpg')
    image = cv2.resize(image, dsize=None, fx=0.15, fy=0.15)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    cv2.namedWindow('trackbars')
    cv2.createTrackbar('H min', 'trackbars', 0, 179, nothing)
    cv2.createTrackbar('H max', 'trackbars', 18, 179, nothing)
    cv2.createTrackbar('S min', 'trackbars', 130, 255, nothing)
    cv2.createTrackbar('S max', 'trackbars', 218, 255, nothing)
    cv2.createTrackbar('V min', 'trackbars', 0, 255, nothing)
    cv2.createTrackbar('V max', 'trackbars', 255, 255, nothing)

    while True:
        h_min = cv2.getTrackbarPos('H min', 'trackbars')
        h_max = cv2.getTrackbarPos('H max', 'trackbars')
        s_min = cv2.getTrackbarPos('S min', 'trackbars')
        s_max = cv2.getTrackbarPos('S max', 'trackbars')
        v_min = cv2.getTrackbarPos('V min', 'trackbars')
        v_max = cv2.getTrackbarPos('V max', 'trackbars')

        thresholded = cv2.inRange(image_hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))

        cv2.imshow('image', image)
        cv2.imshow('thresholded', thresholded)
        cv2.waitKey(100)


main()
