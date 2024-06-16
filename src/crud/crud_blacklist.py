

from sqlalchemy.orm import Session
from src import schemas
from src.db import models

def add_to_blacklist(db: Session, plate_id: int):
    db_blacklist = models.Blacklist(plate_id=plate_id)
    db.add(db_blacklist)
    db.commit()
    db.refresh(db_blacklist)
    return db_blacklist

def remove_from_blacklist(db: Session, plate_id: int):
    db_blacklist = db.query(models.Blacklist).filter(models.Blacklist.plate_id == plate_id).first()
    if db_blacklist:
        db.delete(db_blacklist)
        db.commit()
    return db_blacklist