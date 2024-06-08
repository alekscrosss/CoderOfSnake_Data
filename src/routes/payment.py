from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db.models import ParkingSession, Vehicle

router = APIRouter()


@router.post("/make-payment/")
async def make_payment(
        license_plate: str = Form(...),
        payment_amount: float = Form(...),
        db: Session = Depends(get_db)
):
    try:
        # Find the unpaid parking session by license plate
        db_parking_session = db.query(ParkingSession).join(Vehicle).filter(
            Vehicle.license_plate == license_plate,
            ParkingSession.payment_status == 'not paid'
        ).first()

        if not db_parking_session:
            return JSONResponse(
                content={"error": "Не найдена сессия парковки для данного номерного знака или уже оплачена"},
                status_code=404)

        # Log the expected and provided amounts
        print(f"Expected amount: {db_parking_session.amount_due}, Provided amount: {payment_amount}")
        print(
            f"Expected amount type: {type(db_parking_session.amount_due)}, Provided amount type: {type(payment_amount)}")

        # Check if the payment amount is correct
        if round(float(db_parking_session.amount_due), 2) == round(payment_amount, 2):
            db_parking_session.payment_status = 'paid'
            db.commit()
            db.refresh(db_parking_session)
            return JSONResponse(content={"message": "У вас есть 15 минут для выезда, хорошего пути"})
        else:
            return JSONResponse(content={"error": "Неправильная сумма оплаты"}, status_code=400)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
