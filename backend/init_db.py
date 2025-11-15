from backend.db import get_connection
import psycopg2
from psycopg2.extras import DictCursor

with open("init_db.sql") as f:
    sql = f.read()

conn = get_connection()
cursor = conn.cursor(cursor_factory=DictCursor)

for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("statement executed")

cursor.close()
conn.close()