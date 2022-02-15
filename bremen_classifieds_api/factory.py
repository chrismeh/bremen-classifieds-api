from flask import Flask

from bremen_classifieds_api.blueprints import bp as categories_blueprint
from bremen_classifieds_api.extensions import db, ma


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("bremen_classifieds_api.config")

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    ma.init_app(app)


def register_blueprints(app: Flask):
    app.register_blueprint(categories_blueprint)
