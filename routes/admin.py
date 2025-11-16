from flask import Blueprint, render_template
from auth_utils import login_required

bp = Blueprint("admin", __name__)

@bp.route("/admin")
@login_required
def admin_home():
    return render_template("dashboard.html")
