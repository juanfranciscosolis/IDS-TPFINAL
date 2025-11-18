from flask import Blueprint, jsonify, request
from backend.db import get_connection
from psycopg2.extras import DictCursor

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route('/', methods=['GET'])
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

@usuarios_bp.route('/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (id_usuario,))
    usuario = cursor.fetchone()
    if not usuario:
        return jsonify({"error": "usuario no encontrado"}), 404

    usuario_dict = dict(usuario)
    cursor.close()
    conn.close()
    return jsonify(usuario_dict), 200

@usuarios_bp.route('/', methods=['POST'])

def crear_usuario():
    # Recibe los datos del frontend
    data = request.get_json()
    
    # Se guarda los datos
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    # Conexion con la base de datos
    conn = get_connection()
    cursor = conn.cursor()
    
    # Se guarda el usuario en la base de datos
    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s) RETURNING id",
        (name, email, password)
    )

    # Obtenemos el id
    new_id = cursor.fetchone()[0]

    conn.commit() # Guarda los cambios
    
    cursor.close()
    conn.close()
    
    return jsonify({"id": new_id, "message": "Usuario creado"}), 201