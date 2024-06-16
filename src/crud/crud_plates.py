# src/crud/crud_plates.py

from sqlalchemy.orm import Session
from src.db import models
from src.schemas import schemas_user

def add_vehicle(db: Session, vehicle: schemas_user.VehicleCreate):
    db_vehicle = models.Vehicle(license_plate=vehicle.license_plate)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: int):
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if db_vehicle:
        db.delete(db_vehicle)
        db.commit()
    return db_vehicle
