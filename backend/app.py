from flask import Flask
from flask_cors import CORS
from backend.routes.habitaciones import habitaciones_bp
from backend.routes.reservas import reservas_bp
from backend.routes.usuarios import usuarios_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(habitaciones_bp, url_prefix="/habitaciones")
app.register_blueprint(reservas_bp, url_prefix="/reservas")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

if __name__ == "__main__":
    app.run(port=5010, debug=True)
