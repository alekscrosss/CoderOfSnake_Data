from fastapi import APIRouter
from src.services import reports
from datetime import datetime
import os

router = APIRouter(prefix="/reports", tags=['admin_reports'])

@router.post("/make-admin-repots-all_data/")
async def admin_report_all():
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f'all_users_for_admin_{current_datetime}.csv'

    all_users_for_admin = reports.report_csv(
    host='localhost',
    database= 'db3',
    user='postgres',
    password='567234',
    table_name='users',
    file_name=report_name,
    output_folder='reports_uploads'
)
    return  all_users_for_admin


@router.post("/make-admin-repots-users/")
async def admin_report_users():
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f'users_for_admin_{current_datetime}.csv'

    all_users_for_admin_users = reports.report_csv(
    host='localhost',
    database= 'db3',
    user='postgres',
    password='567234',
    table_name='users',
    file_name=report_name,
    output_folder='reports_uploads',
    selected_columns=["username"]
)
    return  all_users_for_admin_users
