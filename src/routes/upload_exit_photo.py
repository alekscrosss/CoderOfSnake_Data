from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
from datetime import datetime
import uuid
from src.services.image_processing import add_date_to_image
from src.db.database import get_db
from src.crud.crud_parking_session import update_parking_session_exit_time
from src.db.models import ParkingSession, Vehicle
from plate_operation.finish_car_plate_code_building import car_plate_build  # Імпортуємо функцію розпізнавання номерного знака


router = APIRouter()


def save_file(file: UploadFile, filename: str):
    # Ensure the upload directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as buffer:
        buffer.write(file.file.read())


def calculate_amount_due(entry_time: datetime, exit_time: datetime, rate_per_hour: float) -> float:
    duration = exit_time - entry_time
    duration_hours = duration.total_seconds() / 3600
    amount_due = round(duration_hours * rate_per_hour, 2)
    print(f"Calculated amount due: {amount_due}, type: {type(amount_due)}")
    return amount_due


@router.post("/upload-exit-photo")
async def upload_exit_photo(
        exit_photo: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        # Generate a unique filename for the uploaded photo
        unique_filename = f"uploads/{uuid.uuid4().hex}_{exit_photo.filename}"
        save_file(exit_photo, unique_filename)

        # Виклик функції розпізнавання номерного знака
        license_plate = car_plate_build(unique_filename).strip()
        if not license_plate:
            return JSONResponse(content={"error": "Номер не визначено"}, status_code=400)

        # Find the parking session by license plate
        db_parking_session = db.query(ParkingSession).join(Vehicle).filter(
            Vehicle.license_plate == license_plate,
            ParkingSession.exit_time == None
        ).first()

        if not db_parking_session:
            return JSONResponse(content={"error": "Немає сеансу паркування за номером"}, status_code=404)

        exit_time = datetime.now()

        add_date_to_image(unique_filename, exit_time)

        # Calculate the amount due
        rate_per_hour = 25  # standard rate
        amount_due = calculate_amount_due(db_parking_session.entry_time, exit_time, rate_per_hour)

        # Update the parking session with the exit time and amount due
        update_parking_session_exit_time(db, db_parking_session.id, exit_time, amount_due)

        return JSONResponse(content={"message": "Фото завантажено успішно", "exit_time": exit_time.isoformat(), "amount_due": amount_due})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
