from sqlalchemy.orm import Session
from src.db.models import Vehicle

def get_vehicle_by_license_plate(db: Session, license_plate: str):
    return db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()

def create_vehicle(db: Session, license_plate: str):
    db_vehicle = Vehicle(license_plate=license_plate)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle
