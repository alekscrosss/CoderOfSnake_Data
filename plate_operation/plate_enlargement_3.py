"""
Функція car_plate_enlargement масштабує зображення на заданий відсоток і повертає збільшене зображення.
"""

import cv2
import matplotlib.pyplot as plt


def car_plate_enlargement(car_photo, percentage_increase):
    w = int(car_photo.shape[1] * percentage_increase )
    h = int(car_photo.shape[0] * percentage_increase )
    
    # Створення кортежу з новими розмірами
    new_size = (w, h)
    plt.axis('off')  
    
    resize_image = cv2.resize(car_photo, 
                              new_size, 
                              interpolation=cv2.INTER_AREA)
    return resize_image
