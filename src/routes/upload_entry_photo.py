from fastapi import APIRouter, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import random
from datetime import datetime, timedelta
import os
import re
import uuid  # Import uuid for unique filename generation
from src.services.image_processing import add_date_to_image
from src.db.database import get_db
from src.crud.crud_vehicle import get_vehicle_by_license_plate, create_vehicle
from src.crud.crud_parking_session import create_parking_session
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from plate_operation.finish_car_plate_code_building import car_plate_build  # Імпортуємо функцію розпізнавання номерного знака


router = APIRouter()
templates = Jinja2Templates(directory='templates')


def generate_random_date():
    return datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )


def save_file(file: UploadFile, filename: str):
    # Ensure the upload directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as buffer:
        buffer.write(file.file.read())


def is_ukrainian_license_plate(license_plate: str) -> bool:
    # Регулярное выражение для проверки украинских номерных знаков на латинице
    pattern = r"^[A-Z]{2}\d{4}[A-Z]{2}$|^[A-Z]{2}\d{4}[A-Z]{1}$"
    return re.match(pattern, license_plate) is not None


@router.post("/upload-entry-photo")
async def upload_entry_photo(
        entry_photo: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        # Generate a unique filename for the uploaded photo
        unique_filename = f"uploads/{uuid.uuid4().hex}_{entry_photo.filename}"
        save_file(entry_photo, unique_filename)

        # Виклик функції розпізнавання номерного знака
        license_plate = car_plate_build(unique_filename).strip()
        if not license_plate:
            return JSONResponse(content={"error": "Номер не визначено"}, status_code=400)

        date = generate_random_date()
        add_date_to_image(unique_filename, date)

        # Check if the vehicle already exists in the database
        db_vehicle = get_vehicle_by_license_plate(db, license_plate)
        if not db_vehicle:
            # If not, create a new record
            db_vehicle = create_vehicle(db, license_plate)

        # Create a new parking session
        create_parking_session(db, vehicle_id=db_vehicle.id, entry_time=date)

        return JSONResponse(content={"message": "Фото завантажено успішно", "date": date.isoformat(), "license_plate": license_plate})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
