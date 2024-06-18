from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2

router = APIRouter()

class LicensePlateRequest(BaseModel):
    license_plate: str

@router.post("/find-parking-sessions/")
async def find_parking_sessions(request: LicensePlateRequest):
    license_plate = request.license_plate
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='db3',
            user='postgres',
            password='567234'
        )
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM vehicles WHERE license_plate = %s", (license_plate,))
        vehicle_id = cursor.fetchone()

        if vehicle_id is None:
            raise HTTPException(status_code=404, detail="Vehicle not found")

        vehicle_id = vehicle_id[0]

        cursor.execute("SELECT * FROM parking_sessions WHERE vehicle_id = %s", (vehicle_id,))
        parking_sessions = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        if not parking_sessions:
            cursor.close()
            connection.close()
            return {"message": "No parking sessions found for the given vehicle ID"}

        modified_parking_sessions = []
        for session in parking_sessions:
            session_dict = dict(zip(column_names, session))

            cursor.execute("SELECT license_plate FROM vehicles WHERE id = %s", (session_dict['vehicle_id'],))
            license_plate = cursor.fetchone()
            session_dict['vehicle_id'] = license_plate[0] if license_plate else None

            cursor.execute("SELECT username FROM users WHERE id = %s", (session_dict['user_id'],))
            username = cursor.fetchone()
            session_dict['user_id'] = username[0] if username else None

            modified_parking_sessions.append(session_dict)

        cursor.close()
        connection.close()

        return {"parking_sessions": modified_parking_sessions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
