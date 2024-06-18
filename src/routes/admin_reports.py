from fastapi import APIRouter, Depends, HTTPException
from src.services import reports
from datetime import datetime
from fastapi.responses import FileResponse
import os
from src.services.auth import get_current_user
from src.schemas.schemas_user import User

router = APIRouter(prefix="/reports", tags=['admin_reports'])

@router.post("/make-admin-reports-all_data/")
async def admin_report_all():
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f'all_users_for_admin_{current_datetime}.csv'
    output_folder = 'reports_uploads'

    report_path = reports.report_csv(
        host='localhost',
        database='db3',
        user='postgres',
        password='567234',
        table_name='users',
        file_name=report_name,
        output_folder=output_folder,
        selected_columns=["username", "email", "role", "created_at", "updated_at"]
    )

    file_path = os.path.join(output_folder, report_name)
    return FileResponse(path=file_path, filename=report_name, media_type='text/csv')

@router.post("/make-admin-reports-users/")
async def admin_report_users(current_admin: User = Depends(get_current_user)):
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f'users_for_admin_{current_datetime}.csv'
    output_folder = 'reports_uploads'

    report_path = reports.report_csv(
        host='localhost',
        database='db3',
        user='postgres',
        password='567234',
        table_name='users',
        file_name=report_name,
        output_folder=output_folder,
        selected_columns=["username"]
    )

    file_path = os.path.join(output_folder, report_name)
    return FileResponse(path=file_path, filename=report_name, media_type='text/csv')
