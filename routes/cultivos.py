# routes/cultivos.py
from flask import Blueprint
from auth_utils import login_required

bp = Blueprint("cultivos", __name__)

@bp.route("/")
@login_required
def cultivos_home():
    return "Módulo de cultivos (CRUD pendiente)"
