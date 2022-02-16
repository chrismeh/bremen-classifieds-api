import mysql.connector
import requests
from celery import Celery
from environs import Env

from bremen_classifieds_api.classifieds.categories import Category
from bremen_classifieds_api.classifieds.client import Client
from bremen_classifieds_api.classifieds.db import CategoryRepository, ClassifiedRepository

env = Env()
env.read_env()

app = Celery(__name__)
app.config_from_object("bremen_classifieds_api.bin.tasks.config")


@app.task
def update_categories():
    db = connect_to_database()

    client = Client(requests.session())
    category_repo = CategoryRepository(db)

    category_repo.insert_many(client.get_categories())

    categories = category_repo.find_all()
    db.close()

    for category in categories:
        update_classifieds.apply_async((category,), serializer="pickle")


@app.task
def update_classifieds(category: Category):
    db = connect_to_database()

    client = Client(requests.session())
    classifieds_repo = ClassifiedRepository(db)

    classifieds = client.get_classifieds(category)
    classifieds_repo.insert_many(category, classifieds)

    db.close()


def connect_to_database() -> mysql.connector.MySQLConnection:
    return mysql.connector.connect(
        host=env.str("MYSQL_HOST", "localhost"),
        port=env.int("MYSQL_PORT", 3306),
        user=env.str("MYSQL_USER", ""),
        password=env.str("MYSQL_PASSWORD", ""),
        database=env.str("MYSQL_DB", ""),
        autocommit=env.bool("MYSQL_AUTOCOMMIT", True)
    )
