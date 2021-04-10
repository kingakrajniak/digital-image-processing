# algorithm for putting image of a pug in any given place on the art gallery picture (in place of other art preferably)

import cv2
import numpy as np


def handle_mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append([x, y])


def main():
    gallery = cv2.imread('gallery.png')
    gallery = cv2.resize(gallery, dsize=None, fx=.8, fy=.8)
    pug = cv2.imread('pug.png')
    pugy, pugx, c = pug.shape
    galy, galx, c = gallery.shape

    # lg, pg, pd, ld
    pug_points = np.float32([[0, 0], [pugx, 0], [pugx, pugy], [0, pugy]])
    clicked_points = []

    cv2.namedWindow('gallery')
    cv2.setMouseCallback('gallery', handle_mouse_event, clicked_points)

    while True:
        if len(clicked_points) == 4:
            print('Processing...')
            clicked_points1 = clicked_points

            matrix = cv2.getPerspectiveTransform(pug_points, np.float32(clicked_points))  # macierz zmiany
            pug1 = cv2.warpPerspective(pug, matrix, (galx, galy))  # zmieniamy perspektywę obrazka pug

            gallery1 = gallery.copy()
            gallery1 = cv2.fillPoly(gallery1, np.array([clicked_points1]), 0)  # wypełniamy miejsce po obrazie czarnym kolorem

            result = cv2.add(gallery1, pug1)  # dodajemy dwa obrazy
            cv2.imshow('result', result)

        cv2.imshow('gallery', gallery)
        cv2.waitKey(50)


main()
