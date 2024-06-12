"""
основне завдання цього коду - завантажити зображення, 
конвертувати його у формат RGB, 
відобразити його на екрані та повернути конвертоване зображення
"""

import cv2
import matplotlib.pyplot as plt

def open_photo(photo_path):
    #Зчитуємо зображення за допомогою OpenCV
    car_photo = cv2.imread(photo_path)

    if car_photo is None:
        print("The program did not detect the car photo.")
        return None
    # Конвертація фото з BGR в RGB
    # Це потрібно тому що  Matplotlib працю саме з RGB
    car_photo_rgb = cv2.cvtColor(car_photo, cv2.COLOR_BGR2RGB)

    plt.imshow(car_photo_rgb)
    plt.axis('off')  
    plt.show() #Це потрібно для перевірки, коли все буде ОК - приберемо 
    
    #Вертаємо зображення у форматі RGB
    # return car_photo_rgb
    return cv2.imread(photo_path)
