from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas import schemas_user
from src.crud import crud_plates, crud_parking_history
from src.db.database import get_db
from src.services.auth import get_current_user
from typing import List


router = APIRouter()

@router.get("/plates/", response_model=List[schemas_user.Plate])
def get_user_plates(db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_user)):
    return crud_plates.get_user_plates(db, current_user.id)

@router.get("/parking_history/", response_model=List[schemas_user.ParkingHistory])
def get_parking_history(db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_user)):
    return crud_parking_history.get_parking_history(db, current_user.id)
