import cv2
import glob


def main():
    key = ord('q')
    path = input(f'Proszę podać ścieżkę do plików: ')
    images = [cv2.imread(image) for image in glob.glob(f'{path}*.jpg')]
    # wczytywanie wszystkich obrazow .jpg z folderu podanego w path
    # images = images + [cv2.imread(image) for image in glob.glob(f'{path}*.png')]
    # w razie potrzeby mozna rowniez dodac wczytywanie plikow .png
    numb = len(images) - 1  # dostep do ostatniego indeksu wektora images
    i = 0
    cv2.imshow('kitty', images[i])  # pierwsze wywolanie w celu wystartowania pokazu
    key = cv2.waitKey()
    while key == ord('n') or key == ord('p'):  # dziala tylko przy wcisnieciu p lub n
        if key == ord('n'):
            if i == numb:  # gdy ostatnie zdjecie - przechodzi do pierwszego
                i = 0
            else:
                i = i + 1  # kolejne
        if key == ord('p'):
            if i == 0:  # pierwsze zdjecie - wraca do ostatniego
                i = numb
            else:
                i = i - 1  # wczesniejsze
        cv2.imshow('kitty', images[i])  # wywolanie odpoiwedniego obrazu
        key = cv2.waitKey()  # czas na odpowiedz uzytkownika


if __name__ == '__main__':
    main()
