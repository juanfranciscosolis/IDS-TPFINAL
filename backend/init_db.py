import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", 5432)
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    db_name = os.getenv("DB_NAME")
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute(f'CREATE DATABASE {db_name}')
        print(f"Database {db_name} created")
    
    cursor.close()
    conn.close()

def init_tables():
    with open("init_db.sql") as f:
        sql = f.read()

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", 5432)
    )
    cursor = conn.cursor()

    for statement in sql.split(";"):
        if statement.strip():
            cursor.execute(statement)
            conn.commit()

    cursor.close()
    conn.close()
    print("Tables created")

if __name__ == "__main__":
    create_database()
    init_tables()