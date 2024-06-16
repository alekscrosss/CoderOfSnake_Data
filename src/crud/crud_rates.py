# src/crud/crud_rates.py

from sqlalchemy.orm import Session
from src.db import models
from src.schemas import schemas_user

def set_parking_rate(db: Session, rate: schemas_user.ParkingRateCreate):
    db_rate = models.Rate(
        rate_per_hour=rate.rate_per_hour,
        rate_per_min=rate.rate_per_min,
        rate_per_day=rate.rate_per_day,
        rate_per_mon=rate.rate_per_mon
    )
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

def get_parking_rates(db: Session):
    return db.query(models.Rate).all()
