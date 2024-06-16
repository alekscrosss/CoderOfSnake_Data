from sqlalchemy.orm import Session
from src.db import models
from src.schemas import schemas_user

def get_vehicle_by_license_plate(db: Session, license_plate: str):
    return db.query(models.Vehicle).filter(models.Vehicle.license_plate == license_plate).first()

def get_user_vehicles(db: Session, user_id: int):
    return db.query(models.Vehicle).join(models.RegisteredUser).filter(models.RegisteredUser.user_id == user_id).all()

def add_vehicle(db: Session, vehicle: schemas_user.VehicleCreate):
    db_vehicle = models.Vehicle(license_plate=vehicle.license_plate)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def create_vehicle(db: Session, license_plate: str):
    vehicle = schemas_user.VehicleCreate(license_plate=license_plate)
    return add_vehicle(db, vehicle)

def delete_vehicle(db: Session, vehicle_id: int):
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if db_vehicle:
        db.delete(db_vehicle)
        db.commit()
    return db_vehicle
