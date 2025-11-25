from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os
import traceback
import sys  # ✅ AGREGAR ESTA LÍNEA

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Clave de sesión (podés dejar esta fija o también moverla a .env si querés)
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

# Ruta de diagnóstico
@app.route('/debug')
def debug():
    try:
        # Verificar si puede importar los módulos
        from backend.routes.usuarios import usuarios_bp
        from backend.routes.habitaciones import habitaciones_bp
        from backend.routes.reservas import reservas_bp
        
        # Verificar conexión a BD
        from backend.db import get_connection
        conn = get_connection()
        db_status = "connected" if conn else "failed"
        if conn:
            conn.close()
        
        info = {
            "status": "ok",
            "python_path": sys.path,
            "db_connection": db_status,
            "imports_working": True
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

# Registrar blueprints con manejo de errores detallado
try:
    from backend.routes.habitaciones import habitaciones_bp
    from backend.routes.reservas import reservas_bp
    from backend.routes.usuarios import usuarios_bp

    app.register_blueprint(habitaciones_bp, url_prefix="/habitaciones")
    app.register_blueprint(reservas_bp, url_prefix="/reservas")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    
    print("✅ Blueprints registrados correctamente")
    
except Exception as e:
    print(f"❌ Error registrando blueprints: {e}")
    traceback.print_exc()

if __name__ == "__main__":
    app.run(port=5010, debug=True)