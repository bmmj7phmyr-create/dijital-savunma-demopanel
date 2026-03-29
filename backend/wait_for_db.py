import time
import psycopg2
import os

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "db"
DB_PORT = "5432"

while True:
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.close()
        print("Database is ready!")
        break
    except psycopg2.OperationalError:
        print("Waiting for database...")
        time.sleep(2)