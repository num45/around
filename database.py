# database.py
import logging
import psycopg2
from psycopg2 import sql
from tkinter import messagebox

def check_database_connection():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        connection.close()
        messagebox.showinfo("Success", "Database connection successful!")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot connect to the database: {e}")

def create_table():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            salary NUMERIC,
            department VARCHAR(100),
            position VARCHAR(100),
            tel VARCHAR(20),
            email VARCHAR(100),
            dob DATE,
            age INT,
            start_day DATE,
            religion VARCHAR(50),
            nationality VARCHAR(50)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        messagebox.showinfo("Success", "Table 'employees' is ready.")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating table: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

import logging

# ตั้งค่าการบันทึก logging
logging.basicConfig(level=logging.DEBUG)

def add_employee(employee):
    connection = None
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        logging.debug("Database connected successfully.")
        connection.autocommit = True
        cursor = connection.cursor()
        logging.debug("Cursor created successfully.")
        print(employee)
        insert_query = """
            INSERT INTO employees (first_name, last_name, salary, department, position, tel, email, dob, age, start_day, religion, nationality)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            employee['first_name'],
            employee['last_name'],
            employee['salary'],
            employee['department'],
            employee['position'],
            employee['tel'],
            employee['email'],
            employee['dob'],
            employee['age'],
            employee['start_day'],
            employee['religion'],
            employee['nationality']
        ))
        logging.debug("Data inserted successfully.")
        print(cursor.query)  # แสดงคำสั่ง SQL ออกมา
        messagebox.showinfo("Success", f"Employee {employee['first_name']} {employee['last_name']} added to the database!")
    except Exception as e:
        logging.error(f"Error: {e}")  # เพิ่มการพิมพ์ข้อผิดพลาด
        if connection:
            connection.rollback()  # Rollback if there was an error
        messagebox.showerror("Error", f"Error adding employee to database: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        logging.debug(f"Connection status after insert: {connection.status}")

    print(f"Connection status after insert: {connection.status}")

