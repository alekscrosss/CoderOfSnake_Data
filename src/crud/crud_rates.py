from sqlalchemy.orm import Session
from src.schemas import schemas_user
from src.db import models

def set_parking_rate(db: Session, rate: schemas_user.ParkingRateCreate):
    db_rate = models.ParkingRate(amount=rate.amount, duration=rate.duration)
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

def get_parking_rates(db: Session):
    return db.query(models.ParkingRate).all()