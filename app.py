from flask import Flask, render_template
from database import create_database_if_not_exists, initialize_tables
from routes.api import bp as api_bp
from routes.auth import bp as auth_bp
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
# secret key for session handling (used by login/logout)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

# Inicialización DB
with app.app_context():
    create_database_if_not_exists()
    initialize_tables()

# Registrar blueprint de la API
app.register_blueprint(api_bp)
# Registrar blueprint de autenticación (login/logout)
app.register_blueprint(auth_bp)

# Rutas de páginas
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


