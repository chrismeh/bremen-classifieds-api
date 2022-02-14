from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", "production")
DEBUG = ENV == "development"
JSON_SORT_KEYS = False
CACHE_TYPE = env.str("CACHE_TYPE", "SimpleCache")
CACHE_DEFAULT_TIMEOUT = env.int("CACHE_TIMEOUT", 0)

MYSQL_HOST = env.str("MYSQL_HOST", "localhost")
MYSQL_PORT = env.int("MYSQL_PORT", 3306)
MYSQL_USER = env.str("MYSQL_USER", "classifieds")
MYSQL_PASSWORD = env.str("MYSQL_PASSWORD", "classifieds")
MYSQL_DB = env.str("MYSQL_DB", "classifieds")
MYSQL_AUTOCOMMIT = env.bool("MYSQL_AUTOCOMMIT", True)
