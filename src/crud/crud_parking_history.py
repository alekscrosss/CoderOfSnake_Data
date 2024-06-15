from sqlalchemy.orm import Session
from src import schemas
from src.db import models


def get_parking_history(db: Session, user_id: int):
    return db.query(models.ParkingHistory).filter(models.ParkingHistory.user_id == user_id).all()