from flask import Flask
from application.routes import routes  # importa as rotas

def create_app():
    app = Flask(__name__)

    # Registra blueprints, configs, etc
    app.register_blueprint(routes)

    return app