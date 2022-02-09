from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", "production")
DEBUG = ENV == "development"
JSON_SORT_KEYS = False
