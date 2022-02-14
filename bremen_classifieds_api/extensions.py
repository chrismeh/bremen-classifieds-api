import pymysql
import pymysql.cursors
from flask import _app_ctx_stack, current_app
from flask_caching import Cache
from flask_marshmallow import Marshmallow


class MySQL:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("MYSQL_HOST", "localhost")
        app.config.setdefault("MYSQL_USER", None)
        app.config.setdefault("MYSQL_PASSWORD", None)
        app.config.setdefault("MYSQL_DB", None)
        app.config.setdefault("MYSQL_PORT", 3306)
        app.config.setdefault("MYSQL_AUTOCOMMIT", False)

        if hasattr(app, "teardown_appcontext"):
            app.teardown_appcontext(self.teardown)

    @property
    def connect(self):
        return pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            port=current_app.config["MYSQL_PORT"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DB"],
            autocommit=current_app.config["MYSQL_AUTOCOMMIT"],
            cursorclass=pymysql.cursors.DictCursor,
        )

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "pymysql"):
                ctx.pymysql = self.connect
            return ctx.pymysql

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, "pymysql"):
            ctx.pymysql.close()


cache = Cache()
ma = Marshmallow()
db = MySQL()
