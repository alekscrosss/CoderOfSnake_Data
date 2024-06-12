import cv2
import matplotlib.pyplot as plt
import os
import pytesseract
from plate_operation.open_photo_1 import open_photo  # Крок 1
from plate_operation.discavery_plate_2 import discavery_plate  # Крок 2
from plate_operation.plate_enlargement_3 import car_plate_enlargement  # Крок 3

# Вкажіть шлях до виконуваного файлу Tesseract (оновіть цей шлях відповідно до вашої системи)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\tesseract\tesseract.exe'

def car_plate_build(image_path):
    # Отримання поточної директорії скрипта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Поточна директорія: {current_dir}")



    # Прийняття зображення, яке збережене в папку upload
    input_car_photo = open_photo(photo_path=image_path)
    print("Зображення завантажено.")

    # Перевірка існування каскаду Хаара
    cascade_path = os.path.abspath(os.path.join(current_dir, 'car_number.xml'))
    print(f"Шлях до каскаду Хаара: {cascade_path}")


    if not os.path.exists(cascade_path):
        print(f"Каскад Хаара не знайдено за шляхом: {cascade_path}")
        return None

    cascade = cv2.CascadeClassifier(cascade_path)
    print("Каскад Хаара завантажено.")

    # Перевірка завантаження зображення і каскаду
    if input_car_photo is None:
        print("Зображення не завантажено.")
        return None
    if cascade.empty():
        print("Каскад Хаара не завантажено.")
        return None

    discavery_photo_plate = discavery_plate(input_car_photo, cascade)  # знайшли рамку з фото
    print("Область номера виявлено.")

    discavery_photo_plate = car_plate_enlargement(discavery_photo_plate, 2)  # збільшили її
    print("Область номера збільшено.")


    # plt.axis('off')
    # plt.imshow(carplate_extract_img_gray, cmap='gray')
    # #plt.show() # тимчасово, щоб побачити результат


    carplate_extract_img_gray = cv2.cvtColor(discavery_photo_plate,
                                             cv2.COLOR_RGB2GRAY)


    # Збереження зображення у відтінках сірого з новим ім'ям

    base, ext = os.path.splitext(image_path)
    new_filename = f"{base}_gray{ext}"
    cv2.imwrite(new_filename, carplate_extract_img_gray)

    car_plate = pytesseract.image_to_string(
        carplate_extract_img_gray,
        config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIGKLMNOPQRSTUVXWZ0123456789')

    if car_plate != None:
        return car_plate
    else:
        return "None"



