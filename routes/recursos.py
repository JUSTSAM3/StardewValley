# routes/recursos.py
from flask import Blueprint
from auth_utils import login_required

bp = Blueprint("recursos", __name__)

@bp.route("/")
@login_required
def recursos_home():
    return "Módulo de recursos (CRUD pendiente)"
