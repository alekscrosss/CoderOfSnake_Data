from sqlalchemy.orm import Session
from sqlalchemy import select, join
from src.db.models import ParkingSession, Vehicle, User

def get_parking_history(db: Session, user_id: int):
    stmt = (
        select(
            ParkingSession.id,
            ParkingSession.entry_time,
            ParkingSession.exit_time,
            ParkingSession.payment_status,
            ParkingSession.amount_due,
            ParkingSession.is_registered,
            Vehicle.license_plate.label('vehicle_license_plate'),
            User.username.label('user_name')
        )
        .join(Vehicle, ParkingSession.vehicle_id == Vehicle.id)
        .join(User, ParkingSession.user_id == User.id)
        .where(ParkingSession.user_id == user_id)
    )
    result = db.execute(stmt).all()
    return result
