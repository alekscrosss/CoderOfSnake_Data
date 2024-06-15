from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud
from src.schemas import schemas_user
from src.db.database import get_db
from src.services.auth import get_current_admin  # Обновленный импорт

router = APIRouter()

@router.post("/plates/", response_model=schemas_user.Plate)
def add_plate(plate: schemas_user.PlateCreate, db: Session = Depends(get_db), current_admin: schemas_user.User = Depends(get_current_admin)):
    return crud.crud_plates.add_plate(db, plate)

@router.delete("/plates/{plate_id}", response_model=schemas_user.Plate)
def delete_plate(plate_id: int, db: Session = Depends(get_db), current_admin: schemas_user.User = Depends(get_current_admin)):
    return crud.crud_plates.delete_plate(db, plate_id)

@router.post("/rates/", response_model=schemas_user.ParkingRate)
def set_parking_rate(rate: schemas_user.ParkingRateCreate, db: Session = Depends(get_db), current_admin: schemas_user.User = Depends(get_current_admin)):
    return crud.crud_rates.set_parking_rate(db, rate)

@router.post("/blacklist/", response_model=schemas_user.Blacklist)
def add_to_blacklist(plate_id: int, db: Session = Depends(get_db), current_admin: schemas_user.User = Depends(get_current_admin)):
    return crud.crud_blacklist.add_to_blacklist(db, plate_id)

@router.delete("/blacklist/{plate_id}", response_model=schemas_user.Blacklist)
def remove_from_blacklist(plate_id: int, db: Session = Depends(get_db), current_admin: schemas_user.User = Depends(get_current_admin)):
    return crud.crud_blacklist.remove_from_blacklist(db, plate_id)
