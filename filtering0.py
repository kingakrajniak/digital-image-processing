import cv2
import numpy as np


def apply_filter(image, window_size):
    rows, cols = image.shape
    window_half = window_size // 2  # dzielenie bez reszty
    output_image = np.zeros_like(image)  # obraz z samymi 0 o rozmiarach image
    for row in range(0, rows - window_size):  # na okienko patrzymy od lewego gornego rogu
        for col in range(0, cols - window_size):
            mean_value = np.mean(image[row:row + window_size, col:col+window_size])
            output_image[row + window_half, col + window_half] = mean_value
    return output_image


def apply_median_filter(image, window_size):
    rows, cols = image.shape
    window_half = window_size // 2  # dzielenie bez reszty
    output_image = np.zeros_like(image)  # obraz z samymi 0 o rozmiarach image
    for row in range(0, rows - window_size):  # na okienko patrzymy od lewego gornego rogu
        for col in range(0, cols - window_size):
            flattened = image[row:row + window_size, col:col+window_size].flatten()  # zamieniamy macierz na wektor
            sorted_values = np.sort(flattened)
            middle_index = len(sorted_values) // 2
            output_image[row + window_half, col + window_half] = sorted_values[middle_index]
    return output_image


def apply_kuwahara_filter(image):
    rows, cols = image.shape
    output_image = np.zeros_like(image)  # obraz z samymi 0 o rozmiarach image
    for row in range(0, rows - 5):  # na okienko patrzymy od lewego gornego rogu
        for col in range(0, cols - 5):
            region_1 = image[row:row + 3, col:col + 3]
            region_2 = image[row:row + 3, col + 2: col + 5]
            region_3 = image[row + 2:row + 5, col + 2: col + 5]
            region_4 = image[row + 2:row + 5, col: col + 3]

            mean1, std1 = cv2.meanStdDev(region_1)
            mean2, std2 = cv2.meanStdDev(region_2)
            mean3, std3 = cv2.meanStdDev(region_3)
            mean4, std4 = cv2.meanStdDev(region_4)

            min_std = std1
            min_mean = mean1
            if std2 < min_std:  # XD
                min_std = std2
                min_mean = mean2
            if std3 < min_std:
                min_std = std3
                min_mean = mean3
            if std4 < min_std:
                min_std = std4
                min_mean = mean4

            output_image[row + 2, col + 2] = min_mean
    return output_image


def main():
    image = cv2.imread('lena_noise.bmp', cv2.IMREAD_GRAYSCALE)
    window_size = 3
    output_image = apply_kuwahara_filter(image)
    cv2.imshow('org', image)
    cv2.imshow('filtered', output_image)
    cv2.waitKey()


if __name__ == '__main__':
    main()
