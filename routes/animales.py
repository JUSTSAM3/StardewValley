# routes/animales.py
from flask import Blueprint
from auth_utils import login_required

bp = Blueprint("animales", __name__)

@bp.route("/")
@login_required
def animales_home():
    return "Módulo de animales (CRUD pendiente)"
