import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

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





