from flask import Blueprint, jsonify, request, current_app
from flask_mail import Message
from backend.db import get_connection
from datetime import datetime

reservas_bp = Blueprint("reservas", __name__)


@reservas_bp.route('/', methods=['GET'])
def listar_reservas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            r.*,
            h.nombre AS nombre_habitacion,
            u.nombre AS nombre_usuario
        FROM reservas r
        LEFT JOIN habitaciones h ON r.id_habitacion = h.id
        LEFT JOIN usuarios u ON r.id_usuario = u.id
        ORDER BY r.id DESC
    """)
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reservas), 200


@reservas_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def obtener_reservas_por_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            r.*,
            h.nombre AS nombre_habitacion,
            u.nombre AS nombre_usuario
        FROM reservas r
        LEFT JOIN habitaciones h ON r.id_habitacion = h.id
        LEFT JOIN usuarios u ON r.id_usuario = u.id
        WHERE r.id_usuario = %s
    """, (usuario_id,))
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(reservas), 200


@reservas_bp.route('/', methods=['POST'])
def crear_reserva():
    data = request.get_json() or {}

    # Campos obligatorios
    required_fields = [
        'id_habitacion', 'fecha_entrada', 'fecha_salida',
        'adultos', 'ninos', 'nombre_completo', 'email',
        'metodo_pago'
    ]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({
            "error": f"Faltan campos obligatorios: {', '.join(missing)}"
        }), 400

    # Parse de fechas
    try:
        fecha_entrada = datetime.strptime(data.get('fecha_entrada'), "%Y-%m-%d").date()
        fecha_salida = datetime.strptime(data.get('fecha_salida'), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return jsonify({"error": "Formato de fecha inválido. Usar YYYY-MM-DD"}), 400

    if fecha_salida <= fecha_entrada:
        return jsonify({"error": "La fecha de salida debe ser posterior a la de entrada"}), 400

    # Números
    try:
        id_habitacion = int(data.get('id_habitacion'))
        adultos = int(data.get('adultos'))
        ninos = int(data.get('ninos'))
    except (TypeError, ValueError):
        return jsonify({"error": "id_habitacion, adultos y ninos deben ser numéricos"}), 400

    cantidad_personas = adultos + ninos

    nombre_completo = data.get('nombre_completo')
    email = data.get('email')
    telefono = data.get('telefono')
    metodo_pago = data.get('metodo_pago')
    tarjeta_ultimos4 = data.get('tarjeta_ultimos4')

    noches = (fecha_salida - fecha_entrada).days

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Precio de la habitación
    cursor.execute("SELECT precio_por_dia FROM habitaciones WHERE id = %s", (id_habitacion,))
    hab = cursor.fetchone()
    if not hab:
        cursor.close()
        conn.close()
        return jsonify({"error": "Habitación no encontrada"}), 404

    precio_por_dia = float(hab['precio_por_dia'])
    precio_total = round(precio_por_dia * noches, 2)

    # Buscar usuario por email si existe
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    u = cursor.fetchone()
    id_usuario = u['id'] if u else None

    # Insert en reservas
    cursor.execute("""
        INSERT INTO reservas (
            id_habitacion,
            id_usuario,
            fecha_entrada,
            fecha_salida,
            cantidad_adultos,
            cantidad_ninos,
            cantidad_personas,
            precio_total,
            estado,
            nombre_completo,
            email,
            telefono,
            metodo_pago,
            tarjeta_ultimos4
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        id_habitacion,
        id_usuario,
        fecha_entrada,
        fecha_salida,
        adultos,
        ninos,
        cantidad_personas,
        precio_total,
        'pendiente',
        nombre_completo,
        email,
        telefono,
        metodo_pago,
        tarjeta_ultimos4
    ))

    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()


    # Envío de email de reserva

    try:
        mail = current_app.extensions.get('mail')
        if mail:
            asunto = f"Nueva reserva #{new_id}"

            cuerpo = f"""Se registró una nueva reserva.

Datos de la reserva:
- ID de reserva: {new_id}
- Nombre: {nombre_completo}
- Email del cliente: {email}
- Teléfono: {telefono or '-'}

- Habitación ID: {id_habitacion}
- Check-in: {fecha_entrada}
- Check-out: {fecha_salida}
- Adultos: {adultos}
- Niños: {ninos}
- Total de personas: {cantidad_personas}

- Método de pago: {metodo_pago or '-' }
- Precio total: ${precio_total}
"""

            # Solo a tu casilla (MAIL_DEFAULT_SENDER_EMAIL del .env)
            default_sender = current_app.config.get("MAIL_DEFAULT_SENDER")
            if isinstance(default_sender, tuple) and len(default_sender) == 2:
                destinatarios = [default_sender[1]]
            else:
                destinatarios = ["ids874932@gmail.com"]

            msg = Message(
                subject=asunto,
                recipients=destinatarios,
                body=cuerpo
            )
            mail.send(msg)
    except Exception as e:
        print(f"Error enviando email de reserva {new_id}: {e}")

    return jsonify({
        "id": new_id,
        "precio_total": precio_total,
        "estado": "pendiente",
        "mensaje": "Reserva creada correctamente"
    }), 201