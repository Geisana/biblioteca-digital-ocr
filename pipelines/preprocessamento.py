import cv2
import numpy as np

def grayscale(img):

    img = np.array(img)

    if len(img.shape) == 2:
        # já é grayscale
        return img

    if img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    if img.shape[2] == 4:
        return cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

    return img

def threshold(img):
    if len(img.shape) == 3:
        img = grayscale(img)

    return cv2.threshold(
        img, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]