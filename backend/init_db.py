import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def create_database():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 3306))
    )
    conn.autocommit = True
    cursor = conn.cursor()

    db_name = os.getenv("DB_NAME")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4")
    print(f"Database {db_name} OK (creada o ya existente)")

    cursor.close()
    conn.close()

def init_tables():
   
    sql_path = os.path.join(os.path.dirname(__file__), "init_db.sql")
    with open(sql_path, encoding="utf-8") as f:
        sql = f.read()

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 3306))
    )
    cursor = conn.cursor()

   
    for statement in sql.split(";"):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)
    conn.commit()

    cursor.close()
    conn.close()
    print("Tablas y datos de ejemplo creados")

if __name__ == "__main__":
    create_database()
    init_tables()
