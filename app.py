from flask import Flask, render_template
from database import create_database_if_not_exists, initialize_tables


def create_app():
    app = Flask(__name__)

    #Crea la base si no existe
    create_database_if_not_exists()

    #Crea tablas si no existen
    initialize_tables()

    #Página principal
    @app.route('/')
    def login():
        return render_template("login.html")
    
    @app.route('/about')
    def about():
        return render_template("about.html")
    
    @app.route('/admin')
    def admin():
        return render_template("admin.html")

    return app

#main
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
