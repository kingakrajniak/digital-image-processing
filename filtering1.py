# algorithm with implementation of additional filters incl. Kuwahara filter
import cv2
import time
import numpy as np


def main():
    image = cv2.imread('lena_noise.bmp', cv2.IMREAD_GRAYSCALE)
    # image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    # white3(image)  # co trzeci piksel biały
    # smoothing(image)  # wygładzanie dla skali szarości macierzą 3x3 + porównanie czasu
    # smoothing1(image)  # wygładzanie dla skali szarości + dla kolorowych macierzą 3x3
    # smoothing2(image)  # wygładzanie dla skali szarosci + dla kolorowych dowolną macierzą
    kuwahara(image)  # wygładzanie filtrem Kuwahary dla skali szarości + dla kolorowych dowolną macierzą


def kuwahara(image):
    # wygladzanie filtrem Kuwahary - z zachowaniem krawedzi dowolna macierza
    mat1 = 11
    mat = int((mat1 - 1) / 2)
    image1 = cv2.copyMakeBorder(image, mat, mat, mat, mat, cv2.BORDER_REPLICATE)
    dim = image1.shape
    image2 = image1.copy()
    mean = [0, 0, 0, 0]
    var = [0, 0, 0, 0]
    if len(dim) == 2:
        print('obraz w skali szarości')
        for h in range(mat, dim[0] - mat):  # modyfikujemy tylko piksele oryginalnego obrazu
            for w in range(mat, dim[1] - mat):
                mean[0], var[0] = cv2.meanStdDev(image1[h-mat:h+1, w-mat:w+1])  # obszar 1
                var[0] = var[0] ** 2
                mean[1], var[1] = cv2.meanStdDev(image1[h-mat:h+1, w:w+mat+1])  # obszar 2
                var[1] = var[1] ** 2
                mean[2], var[2] = cv2.meanStdDev(image1[h:h+mat+1, w:w+mat+1])  # obszar 3
                var[2] = var[2] ** 2
                mean[3], var[3] = cv2.meanStdDev(image1[h:h+mat+1, w-mat:w+1])  # obszar 4
                var[3] = var[3] ** 2
                minvar = np.min(var)
                for i in range(0, 4):
                    if var[i] == minvar:
                        image2[h, w] = mean[i]
                        break
    else:
        print('obraz kolorowy')
        for h in range(mat, dim[0] - mat):
            for w in range(mat, dim[1] - mat):
                for col in range(0, dim[2]):  # gdy kolorowy idziemy po 3 kanalach
                    mean[0], var[0] = cv2.meanStdDev(image1[h-mat:h+1, w-mat:w+1, col])  # obszar 1
                    var[0] = var[0] ** 2
                    mean[1], var[1] = cv2.meanStdDev(image1[h-mat:h+1, w:w+mat+1, col])  # obszar 2
                    var[1] = var[1] ** 2
                    mean[2], var[2] = cv2.meanStdDev(image1[h:h+mat+1, w:w+mat+1, col])  # obszar 3
                    var[2] = var[2] ** 2
                    mean[3], var[3] = cv2.meanStdDev(image1[h:h+mat+1, w-mat:w+1, col])  # obszar 4
                    var[3] = var[3] ** 2
                    minvar = np.min(var)
                    for i in range(0, 4):
                        if var[i] == minvar:
                            image2[h, w, col] = mean[i]
                            break
    image2 = image2[mat:dim[0]-mat, mat:dim[1]-mat]
    cv2.imshow('org', image)
    cv2.imshow('kuwahara', image2)
    cv2.waitKey()


def white3(image):
    dim = image.shape
    print(dim)
    image1 = image.copy()
    b = 0  # zaczynamy od piksela pierwszego - 0
    for h in range(0, dim[0]):
        for w in range(b, dim[1], 3):  # zamieniamy co 3 piksel
            image1[h, w] = 255  # zamiana piksela na bialy
            if dim[1] - (w + 1) < 3:  # sprawdzamy, czy jestesmy na koncu wiersza; zwazamy na notacje od 0
                b = dim[1] - (w + 1)  # obliczamy, ile pikseli 'pozostalo' w wierszu
                b = 3 - b - 1  # ustalamy od jakiego piksela zaczynamy
    cv2.imshow('bw', image)
    cv2.imshow('white', image1)
    cv2.waitKey()


def smoothing(image):
    image1 = image.copy()
    dim = image.shape
    t0 = time.perf_counter()
    for h in range(1, dim[0] - 1):  # pomijamy 1 i ostatnia kolumne
        for w in range(1, dim[1] - 1):
            image1[h, w] = image[h-1:h+2, w-1:w+2].sum() / 9
    t11 = time.perf_counter()
    t1 = t11 - t0
    print(f'czas własnego wygładzania wynosi {t1} s')

    t0 = time.perf_counter()
    image2 = cv2.blur(image, (3, 3))
    t11 = time.perf_counter()
    t1 = t11 - t0
    print(f'czas wygładzania OpenCV wynosi {t1} s')

    t0 = time.perf_counter()
    ker = np.ones((3, 3), np.float32) / 9
    image3 = cv2.filter2D(image, -1, ker)
    t11 = time.perf_counter()
    t1 = t11 - t0
    print(f'czas wygładzania Filter2D wynosi {t1} s')
    cv2.imshow('org', image)
    cv2.imshow('smooth', image1)
    cv2.imshow('opencv', image2)
    cv2.imshow('filter2d', image3)
    cv2.waitKey()


def smoothing1(image):
    # wygladzanie macierza 3x3
    dim = image.shape
    print(dim)
    image1 = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_REPLICATE)  # kopia obrazu z ramką
    dim = image1.shape
    image2 = image1.copy()  # kopia potrzebna do nadpisania
    if len(dim) == 2:
        print('obraz w skali szarości')
        for h in range(1, dim[0] - 1):  # modyfikujemy tylko piksele oryginalnego obrazu
            for w in range(1, dim[1] - 1):
                image2[h, w] = image1[h-1:h+2, w-1:w+2].sum() / 9
    else:
        print('obraz kolorowy')
        for h in range(1, dim[0] - 1):
            for w in range(1, dim[1] - 1):
                for col in range(0, dim[2]):  # gdy kolorowy idziemy po 3 kanalach
                    image2[h, w, col] = image1[h-1:h+2, w-1:w+2, col].sum() / 9
    image2 = image2[1:(dim[0]-1), 1:(dim[1]-1)]  # wyciagamy z obrazu to, co potrzebne (bez ramki)
    print(image2.shape)  # wynikowy wymiar sie zgadza
    cv2.imshow('org', image)
    cv2.imshow('smoothed', image2)

    image3 = cv2.blur(image, (3, 3))  # sprawdzenie funkcja opencv
    cv2.imshow('opencv', image3)
    cv2.waitKey()


def smoothing2(image):
    # wygladzanie dowolna macierza
    dim = image.shape
    print(dim)
    mat1 = 7  # wymiar macierzy - liczba nieparzysta
    mat = int((mat1 - 1) / 2)
    image1 = cv2.copyMakeBorder(image, mat, mat, mat, mat, cv2.BORDER_REPLICATE)  # kopia obrazu z ramką
    dim = image1.shape
    image2 = image1.copy()  # kopia potrzebna do nadpisania
    if len(dim) == 2:
        print('obraz w skali szarości')
        for h in range(mat, dim[0] - mat):  # modyfikujemy tylko piksele oryginalnego obrazu
            for w in range(mat, dim[1] - mat):
                image2[h, w] = image1[h-mat:h+mat+1, w-mat:w+mat+1].sum() / (mat1 ** 2)
    else:
        print('obraz kolorowy')
        for h in range(mat, dim[0] - mat):
            for w in range(mat, dim[1] - mat):
                for col in range(0, dim[2]):  # gdy kolorowy idziemy po 3 kanalach
                    image2[h, w, col] = image1[h-mat:h+mat+1, w-mat:w+mat+1, col].sum() / (mat1 ** 2)
    image2 = image2[mat:(dim[0]-mat), mat:(dim[1]-mat)]  # wyciagamy z obrazu to, co potrzebne (bez ramki)
    print(image2.shape)  # wynikowy wymiar sie zgadza
    cv2.imshow('org', image)
    cv2.imshow('smoothed', image2)

    image3 = cv2.blur(image, (mat1, mat1))  # sprawdzenie funkcja opencv
    cv2.imshow('opencv', image3)
    cv2.waitKey()


if __name__ == '__main__':
    main()
