# routes/empleados.py
from flask import Blueprint
from auth_utils import login_required

bp = Blueprint("empleados", __name__)

@bp.route("/")
@login_required
def empleados_home():
    return "Módulo de empleados (CRUD pendiente)"
