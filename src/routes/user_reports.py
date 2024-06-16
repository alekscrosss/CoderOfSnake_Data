from fastapi import APIRouter
from src.services import reports
from datetime import datetime
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/reports", tags=['user_reports'])

@router.post("/make-user-repots-all_data/")
async def user_report_all(user_id):
    user_name = reports.search_user_by_id(user_id)

    if user_name is None:
        return {"error": "User not found"}

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f'test_{user_name}_{current_datetime}.csv'
    output_folder = 'reports_uploads'

    report_path = reports.user_report_all_data(
        host='localhost',
        database= 'db3',
        user='postgres',
        password='567234',
        table_name='parking_sessions',
        file_name=report_name,
        output_folder=output_folder,
        selected_columns=["user_id", "vehicle_id","entry_time", "exit_time", 
                          "amount_due","payment_status"],
        user_id=user_id
)
     # Повний шлях до файлу
    file_path = os.path.join(output_folder, report_name)
    return FileResponse(path=file_path, filename=report_name, media_type='text/csv')

