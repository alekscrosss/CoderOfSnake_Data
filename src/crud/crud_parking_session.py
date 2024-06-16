from sqlalchemy.orm import Session
from datetime import datetime
from src.db.models import ParkingSession

def create_parking_session(db: Session, vehicle_id: int, user_id: int, entry_time: datetime):
    db_parking_session = ParkingSession(vehicle_id=vehicle_id, user_id=user_id, entry_time=entry_time)
    db.add(db_parking_session)
    db.commit()
    db.refresh(db_parking_session)
    return db_parking_session


def update_parking_session_exit_time(db: Session, session_id: int, exit_time: datetime, amount_due: float):
    db_parking_session = db.query(ParkingSession).filter(ParkingSession.id == session_id).first()
    if db_parking_session:
        db_parking_session.exit_time = exit_time
        db_parking_session.amount_due = amount_due
        db_parking_session.payment_status = 'not paid'
        db.commit()
        db.refresh(db_parking_session)
    return db_parking_session
