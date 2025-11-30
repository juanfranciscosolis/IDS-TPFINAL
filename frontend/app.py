from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__, template_folder='template')
app.secret_key = "mi_clave_super_secreta_para_el_tp_123"

API_BASE = "http://localhost:5010" 

@app.route('/contact', methods=['POST'])
def contacto():
    nombre = request.form.get('text')
    email = request.form.get('email')
    asunto = request.form.get('subject')
    mensaje = request.form.get('message')


    flash("Mensaje enviado. Pronto nos pondremos en contacto.", "success")
    return redirect(url_for('contact'))

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

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')



@app.route('/rooms')
def rooms():
    try:
        response = requests.get(f"{API_BASE}/habitaciones", timeout=5)
        response.raise_for_status()  # Lanza excepcion si hay error http
        habitaciones = response.json()
        error = None
    except requests.exceptions.RequestException as e:
        habitaciones = []
        error = "No se pudieron cargar las habitaciones"
    
    return render_template('rooms.html', habitaciones=habitaciones, error=error)
    

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('user', user_id=session['user_id']))

    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    error = "Error interno del servidor"

    if not email or not password:
        return render_template('login.html', 
            error="Email y contraseña son requeridos", 
            email=email), 400
    
    try:
        resp = requests.post(
            f"{API_BASE}/usuarios/login",
            json={"email": email, "password": password}
        )

        if resp.status_code == 200:
            user = resp.json()
            session.update({
                'user_id': user['id'],
                'user_name': user.get('nombre', ''),
                'user_email': user.get('email', '')
            })
            return redirect(url_for('user', user_id=user['id']))

        if resp.status_code == 404:
            error = "Usuario no registrado"
        
        if resp.status_code == 401:
            error = "Credenciales incorrectas"

        return render_template('login.html', 
            error=error, email=email), resp.status_code

    except Exception as e:
        return render_template('login.html', 
            error=error,
            email=email), 500
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method  == 'GET':
        return render_template('register.html')

    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "Datos requeridos"}), 400
        
        name = datos.get('name', '').strip()
        email = datos.get('email', '').strip()
        password = datos.get('password', '')
        confirm_password = datos.get('confirmPassword', '')
        
        if not all([name, email, password]):
            return jsonify({"error": "Todos los campos son requeridos"}), 400
        
        if password != confirm_password:
            return jsonify({"error": "Las contraseñas no coinciden"}), 400
        
        response = requests.post(
            f'{API_BASE}/usuarios/',
            json={"name": name, "email": email, "password": password},
            timeout=5
        )
        
        if response.status_code == 201:
            return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
        else:
            error = response.json().get('error', 'Error en el registro')
            return jsonify({"error": error}), response.status_code
            
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/user/<int:user_id>')
def user(user_id):
    if 'user_id' not in session:
        return redirect(url_for("login"))
    
    try:
        # Obtener usuario
        usuario_res = requests.get(f"{API_BASE}/usuarios/{user_id}", timeout=5)
        if usuario_res.status_code != 200:
            return redirect(url_for("login"))
        usuario = usuario_res.json()

        reservas = []
        reservas_res = requests.get(f"{API_BASE}/reservas/usuario/{user_id}/reservas", timeout=5)
        if reservas_res.status_code == 200:
            reservas = reservas_res.json()

        return render_template("user.html", usuario=usuario, reservas=reservas)
        
    except Exception as e:
        return redirect(url_for("login"))

@app.route('/reservar', methods=['GET', 'POST'])
def reservar():
    # Si no hay usuario logueado, redirigimos a login
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    habitacion_id_preseleccionada = request.args.get('habitacion_id')

    try:
        response = requests.get(f"{API_BASE}/habitaciones", timeout=5)
        habitaciones = response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        habitaciones = []

    if request.method == 'GET':
        habitacion_id = request.args.get('habitacion_id')
        form_data = {
            'habitacion': habitacion_id
        }
        # Mostrar formulario
        return render_template(
            'reservar.html',
            user_name=session.get('user_name'),
            user_email=session.get('user_email'),
            form_data=form_data,
            habitaciones=habitaciones 
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
            user_email=session.get('user_email'),
            habitaciones=habitaciones 
        ), 500

    if resp.status_code == 201:
        data = resp.json()
        success_msg = f"Reserva creada correctamente. N° {data.get('id')} - Total: ${data.get('precio_total')}"
        return render_template(
            'reservar.html',
            success=success_msg,
            user_name=session.get('user_name'),
            user_email=session.get('user_email'),
            form_data=form_data,
            habitaciones=habitaciones
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
        user_email=session.get('user_email'),
        form_data=form_data,
        habitaciones=habitaciones 
    ), resp.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)