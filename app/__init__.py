
import os
from flask import Flask
from sqlalchemy import text

def create_app():
    # Check if debug environment variable was passed
    debug: bool = True
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)
    if FLASK_DEBUG:
        debug = FLASK_DEBUG

    # Create the Flask application instance
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/",
    )

    with app.app_context():

        if debug:
            from app.config.dev import DevConfig
            app.config.from_object(DevConfig)

        else:
            #Cargar archivo de configuración de producción
            pass


        #Inicializar extensiones
        from app.extensions import db

        #Inicializar la base de datos
        db.init_app(app)
        
        #Ejecutar consulta de prueba a la BD
        db.session.execute(text('SELECT 1'))
        print('\n\n-- Conexión correcta a Mysql! -- \n\n')

        #Registrar las rutas
        from app.routes import pages_bp
        from app.routes.clientes import clientes_bp

        app.register_blueprint(pages_bp)
        app.register_blueprint(clientes_bp)

    return app