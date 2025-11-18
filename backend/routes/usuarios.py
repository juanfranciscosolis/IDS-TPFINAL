from flask import Blueprint, jsonify, request
from backend.db import get_connection
from psycopg2.extras import DictCursor

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route('/')
def get_usuarios():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SELECT id, nombre, email FROM usuarios")
    usuarios = cursor.fetchall()
    # Convertir a diccionario para mejor formato JSON
    usuarios_dicts = [dict(usuario) for usuario in usuarios]
    cursor.close()
    conn.close()

    return jsonify(usuarios_dicts), 200
