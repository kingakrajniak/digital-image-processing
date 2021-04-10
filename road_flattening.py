import cv2
import numpy as np


def handle_mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append([x, y])


def main():
    img = cv2.imread('road.jpg')
    img = cv2.resize(img, dsize=None, fx=0.4, fy=0.4)
    clicked_points = []

    cv2.namedWindow('img')
    cv2.setMouseCallback('img', handle_mouse_event, clicked_points)  # parametry przekazuje open cv
    # mowimy co wywolac, jezeli cos sie stanie z myszka
    # img trafia do funkcji jako param - nie musi byc zmienna globalna

    dst_points = np.float32([[0, 0], [500, 0], [500, 500], [0, 500]])  # lista list
    # dst_points = np.array([[0, 0], [500, 0], [500, 500], [0, 500]], dtype=np.float32)
    # lg, pg, pd, ld

    while True:
        if len(clicked_points) == 4:
            print('Processing...')
            print(clicked_points)
            print(dst_points)

            matrix = cv2.getPerspectiveTransform(np.float32(clicked_points), dst_points)  # przyjmuje tylko macierze numpy float32
            result = cv2.warpPerspective(img, matrix, (500, 500))
            cv2.imshow('result', result)

        cv2.imshow('img', img)
        cv2.waitKey(50)  # tutaj open cv uruchamia wewnetrzna petle i obsluguje eventy / callbacki


main()
