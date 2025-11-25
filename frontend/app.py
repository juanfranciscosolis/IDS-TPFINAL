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

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/usuario/<int:user_id>')
def usuario(user_id):
    usuario = obtener_usuario(user_id)
    if not usuario:
        return redirect(url_for("login"))    

    return render_template("user.html", usuario=usuario)

"""endpoint API"""
@app.route('/api/usuario/<int:user_id>')
def api_usuario(user_id):
    usuario = obtener_usuario(user_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario)

@app.route('/api/registrar', methods=["POST"])
def api_registrar_usuario():
    datos = request.json # Obtiene los datos

    # Verifica la contrasena
    if datos["password"] != datos["confirmPassword"]:
        return jsonify({"error": "Las contraseñas no coinciden"}), 400

    # Envia los datos al backend
    response = requests.post(
        f'{API_BASE}/usuarios/',
        json={
            "name": datos["name"],
            "email": datos["email"],
            "password": datos["password"]
        }
    )

    return jsonify(response.json()), response.status_code



if __name__ == '__main__':
    app.run(debug=True, port=5000)

