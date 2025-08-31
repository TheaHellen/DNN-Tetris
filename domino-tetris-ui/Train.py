#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 17:02:21 2024

@author: theahellen
"""

from PIL import Image
import numpy as np
import os



def import_images(array, folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Filter for image files
            try:
                img = Image.open(file_path)  # Open the image
                img_array = np.array(img)  # Convert the image to a numpy array
                array.append(img_array)  # Add the array to the list
            except Exception as e:
                print(f"Could not open {filename}: {e}")
    
    #converts back into binary
    for image in range(len(array)):
        for row in range(len(array[image])):
            for element in range(len(array[image][row])):
                if array[image][row][element] == 255:
                    array[image][row][element] = 1
    return array

    
train_x = []  # List to store image arrays
folder_path = "/Users/theahellen/Documents/Uni/Year 4/Dissertation/tetris-diss/domino-ui/C:/Train_data/x-grid/"
train_x = import_images(train_x, folder_path)
print(train_x)

train_y = []
folder_path = "/Users/theahellen/Documents/Uni/Year 4/Dissertation/tetris-diss/domino-ui/C:/Train_data/y-nextposition/"
train_y = import_images(train_y, folder_path)
print(train_y)





