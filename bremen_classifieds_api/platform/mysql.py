import mysql.connector

from bremen_classifieds_api.platform.config import Config


def connect(config: Config) -> mysql.connector.MySQLConnection:
    return mysql.connector.connect(
        host=config.mysql_host,
        port=config.mysql_port,
        user=config.mysql_user,
        password=config.mysql_password,
        database=config.mysql_db,
        autocommit=config.mysql_autocommit
    )
