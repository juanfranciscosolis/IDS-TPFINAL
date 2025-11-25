import mysql.connector
import os

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="Alxsss.mysql.pythonanywhere-services.com",
            user="Alxsss",
            password="Contrasenahoteldb123",
            database="Alxsss$hotel_db",
            port=3306
        )
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None