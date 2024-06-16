import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import csv #16/06/2024

load_dotenv()


def report_csv(host, database, user, password, table_name, file_name, output_folder=None, selected_columns=None):
    try:        
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )        
        cursor = conn.cursor()

        if selected_columns is None:
            query_to_db = f"SELECT * FROM {table_name}"
        else:
            columns_str = ", ".join(selected_columns)
            query_to_db = f"SELECT {columns_str} FROM {table_name}"

        cursor.execute(query_to_db)
        
        rows = cursor.fetchall()

        columns_name = []
        for desc in cursor.description:
            columns_name.append(desc[0])

        if output_folder is not None:
            os.makedirs(output_folder, exist_ok=True)
            file_path = os.path.join(output_folder, file_name)
        else:
            file_path = file_name

        df = pd.DataFrame(rows, columns=columns_name)        
        df.to_csv(file_path, index=False)

        print(f"Data from the table '{table_name}' successfully saved to a file '{file_name}'")

    except Exception as e:
        print(f"Error when working with database {e}")

    finally:       
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def user_report_all_data(host, database, user, 
                         password, table_name, file_name, 
                         output_folder, selected_columns, user_id):
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        query = f"SELECT {', '.join(selected_columns)} FROM {table_name} WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        
        file_path = os.path.join(output_folder, file_name)
        
        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)            
            csvwriter.writerow([
                'user_name' if col == 'user_id' else 'license_plate' if col == 'vehicle_id' else col
                for col in selected_columns
            ])
            
            for row in rows:
                row = list(row)                
                if 'user_id' in selected_columns:
                    user_id_index = selected_columns.index('user_id')
                    user_id_value = row[user_id_index]
                    user_name = search_user_by_id(user_id_value)
                    row[user_id_index] = user_name if user_name else 'Unknown'                
                
                if 'vehicle_id' in selected_columns:
                    vehicle_id_index = selected_columns.index('vehicle_id')
                    vehicle_id_value = row[vehicle_id_index]
                    license_plate = search_license_plate_by_vehicle_id(vehicle_id_value)
                    row[vehicle_id_index] = license_plate if license_plate else 'Unknown'
                
                csvwriter.writerow(row)

    except Exception as e:
        print(f"Error when working with database: {e}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    
    return file_path

def search_user_by_id(user_id:int):
    user_name = None
    try:        
        conn = psycopg2.connect(
            host='localhost',
            database='db3',
            user='postgres',
            password='567234'            
        )        
        cursor = conn.cursor()

        query = "SELECT username FROM users WHERE id = %s;"
        cursor.execute(query, (user_id,))       
        
        row = cursor.fetchone()
        if row:
            user_name = row[0]
        else:
            print("User not found.")
        
    

    except Exception as e:
        print(f"Error when working with database {e}")

    finally:       
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return user_name

def search_license_plate_by_vehicle_id(vehicle_id: int):
    license_plate = None
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='db3',
            user='postgres',
            password='567234'
        )
        cursor = conn.cursor()

        query = "SELECT license_plate FROM vehicles WHERE id = %s;"
        cursor.execute(query, (vehicle_id,))
        
        row = cursor.fetchone()
        if row:
            license_plate = row[0]
        else:
            print("Vehicle not found.")
        
    except Exception as e:
        print(f"Error when working with database: {e}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    return license_plate



    



