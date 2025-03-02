import os
import cv2

def save_image(image, path):
    """ Saves an image to a specified path """
    cv2.imwrite(path, image)

def ensure_folder_exists(folder):
    """ Creates a folder if it doesn't exist """
    if not os.path.exists(folder):
        os.makedirs(folder)
