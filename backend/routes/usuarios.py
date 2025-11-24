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
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({"error": "El usuario ya existe"}), 409


    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Usuario creado exitosamente"}), 201
    
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

    user.pop('password', None)  # no devolvemos la contraseña por seguridad
    return jsonify(user), 200