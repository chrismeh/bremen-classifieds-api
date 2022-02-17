from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    api_env: str
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_db: str
    mysql_autocommit: bool
    redis_host: str


def parse_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        api_env=env.str("FLASK_ENV", "production"),
        mysql_host=env.str("MYSQL_HOST", "localhost"),
        mysql_port=env.int("MYSQL_PORT", 3306),
        mysql_user=env.str("MYSQL_USER", ""),
        mysql_password=env.str("MYSQL_PASSWORD", ""),
        mysql_db=env.str("MYSQL_DB", ""),
        mysql_autocommit=env.bool("MYSQL_AUTOCOMMIT", True),
        redis_host=env.str("REDIS_HOST", "localhost")
    )
