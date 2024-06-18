from sqlalchemy.orm import Session
from src.db.models import Blacklist, Vehicle, User

def add_to_blacklist(db: Session, license_plate: str):
    print(f"Fetching vehicle with license plate: {license_plate}") # Debug info
    vehicle = db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
    if vehicle:
        db_blacklist = Blacklist(plate_id=vehicle.id)
        db.add(db_blacklist)
        db.commit()
        db.refresh(db_blacklist)
        print(f"Vehicle {license_plate} added to blacklist.") # Debug info

        # Update user status if user is registered
        registered_user = db.query(User).join(User.registered_vehicles).filter(Vehicle.id == vehicle.id).first()
        if registered_user:
            registered_user.status_ban = True
            db.commit()
            print(f"User {registered_user.username} banned.") # Debug info

        return db_blacklist
    print(f"Vehicle {license_plate} not found.") # Debug info
    return None

def remove_from_blacklist(db: Session, license_plate: str):
    print(f"Fetching vehicle with license plate: {license_plate}") # Debug info
    vehicle = db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
    if vehicle:
        db_blacklist = db.query(Blacklist).filter(Blacklist.plate_id == vehicle.id).first()
        if db_blacklist:
            db.delete(db_blacklist)
            db.commit()
            print(f"Vehicle {license_plate} removed from blacklist.") # Debug info

            # Update user status if user is registered
            registered_user = db.query(User).join(User.registered_vehicles).filter(Vehicle.id == vehicle.id).first()
            if registered_user:
                registered_user.status_ban = False
                db.commit()
                print(f"User {registered_user.username} unbanned.") # Debug info

            return db_blacklist
    print(f"Blacklist entry for vehicle {license_plate} not found.") # Debug info
    return None
