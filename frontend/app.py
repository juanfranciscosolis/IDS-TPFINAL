from flask import Flask, jsonify, render_template, request, redirect, url_for, session


import requests

app = Flask(__name__, template_folder='template')
app.secret_key = "mi_clave_super_secreta_para_el_tp_123"

API_BASE = "http://localhost:5010" 

def obtener_usuario(id):
    res = requests.get(f"{API_BASE}/usuarios/{id}")
    if res.status_code == 200:
        return res.json()
    return None

def registrar_usuario(datos):
    """
    Funcion auxiliar (recibe JSON)
    """
    if datos["password"] != datos["confirmPassword"]:
        return {"error": "Las contraseñas no coinciden"}, 400
    
    response = requests.post(
        f'{API_BASE}/usuarios/',
        json={
            "name": datos["name"],
            "email": datos["email"], 
            "password": datos["password"]
        }
    )
    
    return response.json(), response.status_code

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about-us')
def about():
    return render_template('about-us.html')

@app.route ('/contact')
def contact():
    return render_template('contact.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # GET: mostrar formulario
    if request.method == 'GET':
        return render_template('login.html')

    # POST: procesar login
    email = request.form.get('email')
    password = request.form.get('password')

    resp = requests.post(
        f"{API_BASE}/usuarios/login",
        json={"email": email, "password": password}
    )

    if resp.status_code == 200:
        user = resp.json()
        session['user_id'] = user['id']
        session['user_name'] = user['nombre']
        session['user_email'] = user['email']
        return redirect(url_for('index'))

    try:
        data = resp.json()
        error = data.get("error", "Error al iniciar sesión")
    except Exception:
        error = "Error al iniciar sesión"

    return render_template('login.html', error=error, email=email), resp.status_code

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    datos = request.get_json()
    resultado, status_code = registrar_usuario(datos)
    
    return jsonify(resultado), status_code

@app.route('/usuario/<int:user_id>')
def usuario(user_id):
    usuario = obtener_usuario(user_id)
    if not usuario:
        return redirect(url_for("login"))    

    return render_template("user.html", usuario=usuario)

@app.route('/api/usuario/<int:user_id>')
def api_usuario(user_id):
    usuario = obtener_usuario(user_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario)

@app.route('/reservar', methods=['GET', 'POST'])
def reservar():
    # Si no hay usuario logueado, redirigimos a login
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        # Mostrar formulario
        return render_template(
            'reservar.html',
            user_name=session.get('user_name'),
            user_email=session.get('user_email')
        )

    # POST: datos del form
    fecha_entrada = request.form.get('fecha_entrada')
    fecha_salida = request.form.get('fecha_salida')
    habitacion_id = request.form.get('habitacion')
    adultos = request.form.get('adultos')
    ninos = request.form.get('ninos')

    nombre_completo = request.form.get('nombre_completo')
    email = request.form.get('email')
    telefono = request.form.get('telefono')

    metodo_pago = request.form.get('metodo_pago')
    numero_tarjeta = (request.form.get('numero_tarjeta') or "").replace(" ", "")
    tarjeta_ultimos4 = numero_tarjeta[-4:] if len(numero_tarjeta) >= 4 else None

    payload = {
        "id_habitacion": habitacion_id,
        "fecha_entrada": fecha_entrada,
        "fecha_salida": fecha_salida,
        "adultos": adultos,
        "ninos": ninos,
        "nombre_completo": nombre_completo,
        "email": email,
        "telefono": telefono,
        "metodo_pago": metodo_pago,
        "tarjeta_ultimos4": tarjeta_ultimos4
    }

    try:
        resp = requests.post(f"{API_BASE}/reservas/", json=payload)
    except requests.RequestException:
        return render_template(
            'reservar.html',
            error="No se pudo conectar con el servidor de reservas.",
            user_name=session.get('user_name'),
            user_email=session.get('user_email')
        ), 500

    if resp.status_code == 201:
        data = resp.json()
        success_msg = f"Reserva creada correctamente. N° {data.get('id')} - Total: ${data.get('precio_total')}"
        return render_template(
            'reservar.html',
            success=success_msg,
            user_name=session.get('user_name'),
            user_email=session.get('user_email')
        )

    # Algún error de validación / negocio
    try:
        data = resp.json()
        error_msg = data.get('error', 'Error al procesar la reserva')
    except ValueError:
        error_msg = 'Error al procesar la reserva'

    return render_template(
        'reservar.html',
        error=error_msg,
        user_name=session.get('user_name'),
        user_email=session.get('user_email')
    ), resp.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)

