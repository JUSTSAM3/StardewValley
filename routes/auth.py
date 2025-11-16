from flask import Blueprint, render_template, request, redirect, url_for, session, flash

bp = Blueprint("auth", __name__)

# --- LOGIN ---
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        if username == "admin" and password == "admin":
            session["logged_in"] = True
            return redirect("/admin")  

        flash("Usuario o contraseña incorrectos", "danger")
        return render_template("login.html")

    return render_template("login.html")


# --- LOGOUT ---
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
