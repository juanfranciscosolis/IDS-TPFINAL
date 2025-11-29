from flask import Blueprint, jsonify, request
from backend.db import get_connection

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route('/', methods=['GET'])
def get_usuarios():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, email FROM usuarios")
        usuarios = cursor.fetchall()
        return jsonify(usuarios), 200
        
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@usuarios_bp.route('/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    if id_usuario <= 0:
        return jsonify({"error": "ID de usuario inválido"}), 400

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify(usuario), 200

    except Exception:
        return jsonify({"error": "Error del servidor"}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos requeridos"}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Nombre, email y password son obligatorios"}), 400

    conn = None
    cursor = None
    try:
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
        
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"error": "Error del servidor"}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@usuarios_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Datos requeridos"}), 400
        
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email y password son obligatorios"}), 400

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT id, nombre, email, password FROM usuarios WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        if user['password'] != password:
            return jsonify({"error": "Credenciales invalidas"}), 401
        
        user.pop('password', None)
        
        return jsonify(user), 200

    except Exception as e:
        return jsonify({"error": "Error del servidor"}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()