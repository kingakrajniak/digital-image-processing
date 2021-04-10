# algorithm for counting gummies of 2 different colours and 2 different shapes

import argparse
import json
from pathlib import Path
import numpy as np
import cv2


def perform_processing(image):
    image = cv2.resize(image, dsize=None, fx=0.15, fy=0.15)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    kernel = np.ones((3, 3), np.uint8)

    # zielone misie
    green_bears = cv2.inRange(image_hsv, (22, 139, 40), (31, 255, 255))  # maska na zielone misie
    green_bears = cv2.morphologyEx(green_bears, cv2.MORPH_OPEN, kernel)
    green_bears = cv2.morphologyEx(green_bears, cv2.MORPH_CLOSE, kernel)  # operacja domkniecia

    contours_gb, _ = cv2.findContours(green_bears, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # znajdujemy kontury
    # print(f' Jest {gb_count} zielonych misiów.')
    # cv2.drawContours(image, contours_gb, -1, (0, 0, 255), thickness=2)  # tu bysmy rysowali kontury
    gb_count = len(contours_gb)  # liczba zielonych misiow

    # zielone dropsy
    green_drops = cv2.inRange(image_hsv, (34, 0, 40), (79, 255, 255))  # maska na zielone dropsy
    green_drops = cv2.morphologyEx(green_drops, cv2.MORPH_OPEN, kernel)
    green_drops = cv2.morphologyEx(green_drops, cv2.MORPH_CLOSE, kernel)

    contours_gd, _ = cv2.findContours(green_drops, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(image, contours_gd, -1, (0, 0, 122), thickness=2)
    # print(f' Jest {gd_count} zielonych dropsów.')
    gd_count = len(contours_gd)  # liczba zielonych dropsow

    # pomaranczowe
    orange_gummies = cv2.inRange(image_hsv, (0, 130, 0), (18, 218, 255))  # maska na wszystkie pomaranczowe zelki
    orange_gummies = cv2.morphologyEx(orange_gummies, cv2.MORPH_OPEN, kernel)
    orange_gummies = cv2.morphologyEx(orange_gummies, cv2.MORPH_CLOSE, kernel)

    contours_og, _ = cv2.findContours(orange_gummies, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(f' Jest {len(contours_og)} pomarańczowych żelków.')
    og_count = len(contours_og)  # liczba wszystkich pomaranczowych zelkow

    orange_drops = cv2.HoughCircles(orange_gummies, cv2.HOUGH_GRADIENT, 1, 10, param1=1, param2=9, minRadius=10,
                                    maxRadius=20)  # znajdujemy tylko okragle kontury - dropsy

    if orange_drops is not None:
        contours_od = np.uint16(np.around(orange_drops))
        # for i in contours_od[0, :]:
        #     cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)  # tu bysmy rysowali kolka
        contours_od = contours_od[0]
        od_count = len(contours_od)  # liczba pomaranczowych dropsow
    else:
        od_count = 0  # jezeli nie ma pomaranczowych dropsow to ich liczba = 0
    # print(f'Jest {od_count} pomarańczowych dropsów.')

    ob_count = og_count - od_count  # liczba pomaranczowych misiow - roznica wszystkich i dropsow
    # print(f'Jest {ob_count} pomaranczowych misiów.')
    return gd_count, od_count, gb_count, ob_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('images_dir', type=str)
    parser.add_argument('results_file', type=str)
    args = parser.parse_args()

    images_dir = Path(args.images_dir)
    results_file = Path(args.results_file)

    images_paths = sorted([image_path for image_path in images_dir.iterdir() if image_path.name.endswith('.jpg')])
    results = {}
    for image_path in images_paths:
        image = cv2.imread(str(image_path))
        if image is None:
            print(f'Error loading image {image_path}')
            continue

        results[image_path.name] = perform_processing(image)

    with results_file.open('w') as output_file:
        json.dump(results, output_file, indent=4)


if __name__ == '__main__':
    main()
