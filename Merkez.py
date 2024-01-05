import os
import cv2
import pyautogui
import tkinter as tk
from tkinter import filedialog

from Sabitler import Sabitler
from Araclar import Araclar
from Nokta import Nokta
from Daire import Daire

sabitler = Sabitler()

nokta1 = None
nokta2 = None


def isaretciyiCiz(x, y):
    cv2.circle(image, (x, y), Sabitler.isaretci_nokta_capi, Sabitler.isaretci_nokta_rengi, -1)
    cv2.line(image, (x, y - Sabitler.isaretci_cizgi_uzunlugu), (x, y + Sabitler.isaretci_cizgi_uzunlugu),
             Sabitler.isaretci_cizgi_rengi, Sabitler.isaretci_cizgi_kalinligi)
    cv2.line(image, (x - Sabitler.isaretci_cizgi_uzunlugu, y), (x + Sabitler.isaretci_cizgi_uzunlugu, y),
             Sabitler.isaretci_cizgi_rengi, Sabitler.isaretci_cizgi_kalinligi)


def fareTiklamasi(event, x, y, flags, param):
    global nokta1, nokta2
    if event == cv2.EVENT_LBUTTONDOWN:
        print("x: " + str(x) + " - y: " + str(y))

        if nokta1 is None:
            nokta1 = Nokta(x, y)
            isaretciyiCiz(x, y)
            print("Nokta 1 HAZIR")
        elif nokta2 is None:
            nokta2 = Nokta(x, y)
            isaretciyiCiz(x, y)
            print("Nokta 2 HAZIR")


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
file_name = os.path.basename(file_path)
print(file_name)

file_size = file_name.split("-")[1]
file_size = file_size.split(".")[0]
genislik_urun = int(file_size.split("x")[0])
yukseklik_urun = int(file_size.split("x")[1])

image = cv2.imread(file_name, 1)
clone = image.copy()

dimensions = image.shape
yukseklik_resim = dimensions[0]
genislik_resim = dimensions[1]
print(dimensions)

genislik_carpani = genislik_urun / genislik_resim
yukseklik_carpani = yukseklik_urun / yukseklik_resim

pencere_ismi = "image"
cv2.namedWindow(pencere_ismi)
cv2.moveWindow(pencere_ismi, 400, 150)
cv2.setMouseCallback(pencere_ismi, fareTiklamasi)

while True:
    cv2.imshow(pencere_ismi, image)
    key = cv2.waitKey(1) & 0xFF
    # --------------------------------------------------------------------------------------------------
    if key == ord("d"):
        image = clone.copy()
        nokta1 = None
        nokta2 = None

        print("2 nokta seçiniz. Daire Merkezi Üzeri ve Daire Çevresi Üzeri")
    # --------------------------------------------------------------------------------------------------
    elif key == ord("e"):
        print("----------------------------------------------------------")
        print("Hesaplanan Bilgiler: ")

        yaricap = nokta1.distance(nokta2)[2]
        x = nokta1.X * genislik_carpani
        y = nokta1.Y * yukseklik_carpani
        y = yukseklik_urun - y
        print("Yarıçap: " + str(yaricap))
        print("x: " + str(x) + " - y: " + str(y))

    # --------------------------------------------------------------------------------------------------
    # if the 'r' key is pressed, reset
    elif key == ord("r"):
        image = clone.copy()
        nokta1 = None
        nokta2 = None

        print("Ölçüler temizlendi.")
    # --------------------------------------------------------------------------------------------------
    # if the 'x' key is pressed, break from the loop
    elif key == ord("x"):
        break

# close all open windows
cv2.destroyAllWindows()
