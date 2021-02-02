from flask import Flask


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    from app.main import main as main_blueprient
    app.register_blueprint(main_blueprient)

    return app
