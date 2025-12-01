from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os

from backend.routes.habitaciones import habitaciones_bp
from backend.routes.reservas import reservas_bp
from backend.routes.usuarios import usuarios_bp

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)
CORS(app)


app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "c7f1f6e8e9c54b3db5a2f0b0c2a4c3f6e1d9d8f7a6b5c4d3e2f1a0b9c8d7e6f5"
)

# Config de correo leída desde .env
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

default_sender_name = os.getenv("MAIL_DEFAULT_SENDER_NAME", "Hotel IDS")
default_sender_email = os.getenv("MAIL_DEFAULT_SENDER_EMAIL", os.getenv("MAIL_USERNAME"))

app.config['MAIL_DEFAULT_SENDER'] = (default_sender_name, default_sender_email)

# Inicializar extensión de mail
mail = Mail(app)

# Registrar blueprints
app.register_blueprint(habitaciones_bp, url_prefix="/habitaciones")
app.register_blueprint(reservas_bp, url_prefix="/reservas")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

if __name__ == "__main__":
    app.run(port=5010, debug=True)
