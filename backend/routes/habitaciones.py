from flask import Blueprint, jsonify, request
from backend.db import get_connection

habitaciones_bp = Blueprint("habitaciones", __name__)

#Devuelve todas las habitaciones
@habitaciones_bp.route("/")
def get_habitaciones():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM habitaciones")
    habitaciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(habitaciones)

#Devuelve una habitacion en especifico
@habitaciones_bp.route("/int:<habitacion_id>", methods=["GET"])
def get_habitacion(habitacion_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM habitaciones WHERE id = %s", (habitacion_id,))
    habitacion = cursor.fetchone()
    cursor.close()
    conn.close()
    if habitacion is None:
        return jsonify({"Error": "Habitacion no encontrada"}), 404
    return jsonify(habitacion)