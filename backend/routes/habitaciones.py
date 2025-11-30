from flask import Blueprint, jsonify, request
from backend.db import get_connection

habitaciones_bp = Blueprint("habitaciones", __name__)

# Devuelve todas las habitaciones
@habitaciones_bp.route("/", methods=["GET"])
def get_habitaciones():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM habitaciones")
        habitaciones = cursor.fetchall()        
        cursor.close()
        conn.close()
        return jsonify(habitaciones)
    except Exception as e:
        return jsonify({"error": "Error al obtener habitaciones"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
# Devuelve una habitacion en especifico
@habitaciones_bp.route("/<int:habitacion_id>", methods=["GET"])
def get_habitacion(habitacion_id):
    conn = None
    cursor = None
    if habitacion_id <= 0:
        return jsonify({"error": "ID de habitación inválido"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM habitaciones WHERE id = %s", (habitacion_id,))
        habitacion = cursor.fetchone()
        
        if not habitacion:
            return jsonify({"error": "Habitación no encontrada"}), 404
            
        return jsonify(habitacion)
        
    except Exception:
        return jsonify({"error": "Error del servidor"}), 500
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()