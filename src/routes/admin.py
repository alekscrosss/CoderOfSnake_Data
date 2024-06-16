from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud
from src.schemas import schemas_user
from src.db.database import get_db
from src.services.auth import get_current_user
from typing import List
from src.db.models import Role

router = APIRouter()

def get_current_active_user(current_user: schemas_user.User = Depends(get_current_user)):
    if current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Permission denied, admin role required")
    return current_user

@router.post("/vehicles/", response_model=schemas_user.Vehicle)
def add_vehicle(vehicle: schemas_user.VehicleCreate, db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_active_user)):
    return crud.crud_vehicle.add_vehicle(db, vehicle)

@router.delete("/vehicles/{vehicle_id}", response_model=schemas_user.Vehicle)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_active_user)):
    vehicle = crud.crud_vehicle.delete_vehicle(db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.post("/rates/", response_model=schemas_user.ParkingRate)
def set_parking_rate(rate: schemas_user.ParkingRateCreate, db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_active_user)):
    return crud.crud_vehicle.set_parking_rate(db, rate)

@router.get("/rates/", response_model=List[schemas_user.ParkingRate])
def get_parking_rates(db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_active_user)):
    return crud.crud_vehicle.get_parking_rates(db)

@router.post("/blacklist/", response_model=schemas_user.Blacklist)
def add_to_blacklist(vehicle_id: int, db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_active_user)):
    return crud.crud_vehicle.add_to_blacklist(db, vehicle_id)

@router.delete("/blacklist/{plate_id}", response_model=schemas_user.Blacklist)
def remove_from_blacklist(plate_id: int, db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_active_user)):
    return crud.crud_vehicle.remove_from_blacklist(db, plate_id)
