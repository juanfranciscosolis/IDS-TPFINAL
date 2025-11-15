from flask import Blueprint, jsonify, request
from backend.db import get_connection

reservas_bp = Blueprint("reservas", __name__)
