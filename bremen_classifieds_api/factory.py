from flask import Flask

from bremen_classifieds_api.blueprints import bp as categories_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(categories_blueprint)
