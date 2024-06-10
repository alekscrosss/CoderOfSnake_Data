"""
В цій частині коду ми збираємо усі складові аналізу фото і повертаємо результат
"""
import cv2 # Бібліотека OpenCV використовується для комп'ютерного зору
import matplotlib.pyplot as plt # Використовується для візуалізації зображень
import os

from open_photo_1 import open_photo #крок 1
from discavery_plate_2 import discavery_plate #крок 2
from plate_enlargement_3 import car_plate_enlargement #крок 3

photo_name = '1car.jpg'

def car_plate_build():
    #Приймаємо зображення, яке зберіглось у папку upload
    input_car_photo = open_photo(photo_path = f'uploads/{photo_name}')

    cascade = cv2.CascadeClassifier('plate_operation/car_number.xml')

    discavery_photo_plate = discavery_plate(input_car_photo, cascade) # знайшли рамку з фото
    discavery_photo_plate = car_plate_enlargement(discavery_photo_plate, 2) # збільшили її

    plt.imshow(discavery_photo_plate)
    plt.show() # тимчасово, щоб побачити результат

    carplate_extract_img_gray = cv2.cvtColor(discavery_photo_plate, 
                                             cv2.COLOR_RGB2GRAY)
    plt.axis('off')  
    plt.imshow(carplate_extract_img_gray, cmap='gray')
    plt.show() # тимчасово, щоб побачити результат

    # Збереження зображення у відтінках сірого з новим ім'ям

    img_path = f'uploads/{photo_name}'

    base, ext = os.path.splitext(img_path)
    new_filename = f"{base}_gray{ext}"
    cv2.imwrite(new_filename, carplate_extract_img_gray)

test = car_plate_build()
test()

