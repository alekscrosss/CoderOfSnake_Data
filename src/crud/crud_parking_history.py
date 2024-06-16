# src/crud/crud_parking_history.py

from sqlalchemy.orm import Session
from src.db import models

def get_parking_history(db: Session, user_id: int):
    return db.query(models.ParkingSession).filter(models.ParkingSession.user_id == user_id).all()
