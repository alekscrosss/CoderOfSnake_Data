from sqlalchemy.orm import Session
from src.db.models import Vehicle
from src.schemas.schemas_user import PlateCreate

def add_plate(db: Session, plate: PlateCreate):
    db_plate = Vehicle(license_plate=plate.number)
    db.add(db_plate)
    db.commit()
    db.refresh(db_plate)
    return db_plate

def delete_plate(db: Session, plate_id: int):
    db_plate = db.query(Vehicle).filter(Vehicle.id == plate_id).first()
    if db_plate:
        db.delete(db_plate)
        db.commit()
    return db_plate
