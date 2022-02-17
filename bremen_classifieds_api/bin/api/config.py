from bremen_classifieds_api.platform.config import parse_config

config = parse_config()

ENV = config.api_env
DEBUG = ENV == "development"
JSON_SORT_KEYS = False

MYSQL_HOST = config.mysql_host
MYSQL_PORT = config.mysql_port
MYSQL_USER = config.mysql_user
MYSQL_PASSWORD = config.mysql_password
MYSQL_DB = config.mysql_db
MYSQL_AUTOCOMMIT = config.mysql_autocommit
