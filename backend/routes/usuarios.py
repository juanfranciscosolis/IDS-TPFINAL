from flask import Blueprint, jsonify, request
from backend.db import get_connection

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route('/', methods=['GET'])
def get_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, email FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()

    # usuarios ya es una lista de dicts gracias a dictionary=True
    return jsonify(usuarios), 200

@usuarios_bp.route('/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if not usuario:
        return jsonify({"error": "usuario no encontrado"}), 404

    return jsonify(usuario), 200

@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    # Recibe los datos del frontend
    data = request.get_json()

    # Se guardan los datos
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Conexion con la base de datos
    conn = get_connection()
    cursor = conn.cursor()

    # INSERT en MySQL (sin RETURNING)
    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )

    # Obtenemos el id autoincremental generado
    new_id = cursor.lastrowid

    conn.commit()  # Guarda los cambios

    cursor.close()
    conn.close()

    return jsonify({"id": new_id, "message": "Usuario creado"}), 201

@usuarios_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, nombre, email, password FROM usuarios WHERE email = %s",
        (email,)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
   
    if not user:
        return jsonify({"error": "Usuario no existe"}), 404

    if user['password'] != password:
        return jsonify({"error": "Contraseña incorrecta"}), 401

    user.pop('password', None)  # no devolvemos la contraseña
    return jsonify(user), 200