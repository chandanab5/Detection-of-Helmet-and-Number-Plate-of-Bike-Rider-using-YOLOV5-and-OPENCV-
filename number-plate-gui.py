from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt
import easyocr
root = Tk()
root.geometry('750x270')
root.title("Number plate")

def loader():
    global get_image, image_path
    input_path = filedialog.askopenfilename(title="Open Image", filetype = (("JPG",".jpg"), ("All Files", "*.*")))
    image_path = input_path
    if input_path:
        if input_path.endswith(".jpg"):
            get_image = ImageTk.PhotoImage(Image.open(input_path))


            my_label.config(image=get_image)
        else:
            input_path = f'{input_path}.jpg'
            get_image = ImageTk.PhotoImage(Image.open(input_path))
            my_label.config(image=get_image)

def on_click():
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray_img, 11, 17, 17)  # remove noise
    edged = cv2.Canny(bfilter, 30, 200)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    location

    mask = np.zeros(gray_img.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray_img[x1:x2 + 1, y1:y2 + 1]
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    print(result)




my_label = Label(root, text="Open Image", font =("Helvetica, 28"))
my_label.pack(pady=50)
open_button = Button(root, text="Open Image", command=loader)
open_button.pack(pady=10)
click_button=Button(root, text="Click to Extract", command=lambda : on_click(),bg='light yellow')
click_button.pack(pady=15)


root.mainloop()