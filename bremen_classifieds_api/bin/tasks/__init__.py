import requests
from celery import Celery
from celery.signals import worker_ready

from bremen_classifieds_api.classifieds.categories import Category
from bremen_classifieds_api.classifieds.client import Client
from bremen_classifieds_api.classifieds.db import CategoryRepository, ClassifiedRepository
from bremen_classifieds_api.platform.config import parse_config
from bremen_classifieds_api.platform.mysql import connect

app = Celery(__name__)
app.config_from_object("bremen_classifieds_api.bin.tasks.config")
app_config = parse_config()


@worker_ready.connect
def schedule_update_jobs(sender, **kwargs):
    update_categories.delay()


@app.task
def update_categories():
    db = connect(app_config)

    client = Client(requests.session())
    category_repo = CategoryRepository(db)

    category_repo.insert_many(client.get_categories())

    categories = category_repo.find_all()
    db.close()

    for category in categories:
        update_classifieds.apply_async((category,), serializer="pickle")


@app.task
def update_classifieds(category: Category):
    db = connect(app_config)

    client = Client(requests.session())
    classifieds_repo = ClassifiedRepository(db)

    classifieds = client.get_classifieds(category)
    classifieds_repo.insert_many(category, classifieds)

    db.close()
