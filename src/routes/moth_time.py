from fastapi import APIRouter, HTTPException
import psycopg2
from datetime import datetime, timedelta

router = APIRouter(prefix="/moth_time", tags=['moth_time'])


@router.post("/check-parking-time/")
async def check_parking_time(user_id: int):
    try:

        connection = psycopg2.connect(
            host='localhost',
            database='db3',
            user='postgres',
            password='567234'
        )
        cursor = connection.cursor()

        current_year = datetime.now().year
        current_month = datetime.now().month

        cursor.execute("""
            SELECT entry_time, exit_time 
            FROM parking_sessions 
            WHERE user_id = %s 
            AND EXTRACT(YEAR FROM entry_time) = %s 
            AND EXTRACT(MONTH FROM entry_time) = %s
        """, (user_id, current_year, current_month))

        parking_sessions = cursor.fetchall()

        if not parking_sessions:
            return {"message": "No parking sessions found for the given user ID this month"}

        total_parking_time = timedelta()

        for entry_time, exit_time in parking_sessions:
            if exit_time and entry_time:
                total_parking_time += (exit_time - entry_time)

        if total_parking_time > timedelta(hours=700):
            return {"result": False}
        else:
            return {"result": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:

        cursor.close()
        connection.close()
