from sqlalchemy.orm import Session
from src.db import models
from src.schemas import schemas_user
from sqlalchemy.exc import IntegrityError

def get_vehicle_by_license_plate(db: Session, license_plate: str) -> models.Vehicle:
    return db.query(models.Vehicle).filter(models.Vehicle.license_plate == license_plate).first()

def get_user_vehicles(db: Session, user_id: int) -> list[models.Vehicle]:
    return db.query(models.Vehicle).join(models.RegisteredUser).filter(models.RegisteredUser.user_id == user_id).all()

def add_vehicle(db: Session, vehicle: schemas_user.VehicleCreate) -> models.Vehicle:
    existing_vehicle = get_vehicle_by_license_plate(db, vehicle.license_plate)
    if existing_vehicle:
        raise ValueError(f"Vehicle with license plate {vehicle.license_plate} already exists")

    db_vehicle = models.Vehicle(license_plate=vehicle.license_plate)
    db.add(db_vehicle)
    try:
        db.commit()
        db.refresh(db_vehicle)
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Vehicle with license plate {vehicle.license_plate} already exists")

    return db_vehicle

def create_vehicle(db: Session, license_plate: str) -> models.Vehicle:
    vehicle = schemas_user.VehicleCreate(license_plate=license_plate)
    return add_vehicle(db, vehicle)

def delete_vehicle(db: Session, vehicle_id: int) -> models.Vehicle:
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise ValueError(f"Vehicle with id {vehicle_id} not found")
    db.delete(db_vehicle)
    db.commit()
    return db_vehicle

def set_parking_rate(db: Session, rate: schemas_user.ParkingRateCreate):
    db_rate = models.Rate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

def get_parking_rates(db: Session):
    return db.query(models.Rate).all()


def add_to_blacklist(db: Session, plate_id: int, reason: str = None):
    db_blacklist_entry = models.Blacklist(plate_id=plate_id, reason=reason)
    db.add(db_blacklist_entry)
    db.commit()
    db.refresh(db_blacklist_entry)
    return db_blacklist_entry

def remove_from_blacklist(db: Session, plate_id: int):
    db_blacklist_entry = db.query(models.Blacklist).filter(models.Blacklist.plate_id == plate_id).first()
    if db_blacklist_entry:
        db.delete(db_blacklist_entry)
        db.commit()
    return db_blacklist_entry
