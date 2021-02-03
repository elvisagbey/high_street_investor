from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    from app.main import main as main_blueprient
    app.register_blueprint(main_blueprient)

    return app
