from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests

app = Flask(__name__, template_folder='template')

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

@app.route('/login')
def login():
    return render_template('login.html')

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

