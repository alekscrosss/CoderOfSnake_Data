# src/routes/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import crud
from src.schemas import schemas_user
from src.db.database import get_db
from src.services.auth import get_current_user
from typing import List

router = APIRouter()

def verify_admin(current_user: schemas_user.User):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

@router.post("/vehicles/", response_model=schemas_user.Vehicle)
def add_vehicle(vehicle: schemas_user.VehicleCreate, db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_user)):
    verify_admin(current_user)
    return crud.crud_vehicle.add_vehicle(db, vehicle)

@router.delete("/vehicles/{vehicle_id}", response_model=schemas_user.Vehicle)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db), current_admin: schemas_user.User = Depends(get_current_user)):
    verify_admin(current_admin)
    vehicle = crud.crud_vehicle.delete_vehicle(db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.post("/rates/", response_model=schemas_user.ParkingRate)
def set_parking_rate(rate: schemas_user.ParkingRateCreate, db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_user)):
    verify_admin(current_user)
    return crud.crud_rates.set_parking_rate(db, rate)

@router.get("/rates/", response_model=List[schemas_user.ParkingRate])
def get_parking_rates(db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_user)):
    verify_admin(current_user)
    return crud.crud_rates.get_parking_rates(db)

@router.post("/blacklist/", response_model=schemas_user.Blacklist)
def add_to_blacklist(vehicle_id: int, db: Session = Depends(get_db), current_admin: schemas_user.User = Depends(get_current_user)):
    verify_admin(current_admin)
    return crud.crud_blacklist.add_to_blacklist(db, vehicle_id)

@router.delete("/blacklist/{vehicle_id}", response_model=schemas_user.Blacklist)
def remove_from_blacklist(vehicle_id: int, db: Session = Depends(get_db), current_admin: schemas_user.User = Depends(get_current_user)):
    verify_admin(current_admin)
    return crud.crud_blacklist.remove_from_blacklist(db, vehicle_id)
