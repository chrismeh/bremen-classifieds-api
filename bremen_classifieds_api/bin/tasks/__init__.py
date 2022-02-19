import requests
from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready

from bremen_classifieds_api.classifieds.categories import Category
from bremen_classifieds_api.classifieds.client import Client
from bremen_classifieds_api.classifieds.db import CategoryRepository, ClassifiedRepository
from bremen_classifieds_api.classifieds.updater import Updater
from bremen_classifieds_api.platform.config import parse_config
from bremen_classifieds_api.platform.mysql import connect

app = Celery(__name__)
app.config_from_object("bremen_classifieds_api.bin.tasks.config")
app_config = parse_config()


@app.on_after_configure.connect
def schedule_update_jobs(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour="8-20", day_of_week="1-6"),
        update_categories.s()
    )


@worker_ready.connect
def schedule_update_jobs_now(sender, **kwargs):
    update_categories.delay()


@app.task
def update_categories():
    db = connect(app_config)

    updater = Updater(Client(requests.session()), CategoryRepository(db), ClassifiedRepository(db))
    categories = updater.update_categories()
    db.close()

    for category in categories:
        update_classifieds.apply_async((category,), serializer="pickle")


@app.task
def update_classifieds(category: Category):
    db = connect(app_config)

    updater = Updater(Client(requests.session()), CategoryRepository(db), ClassifiedRepository(db))
    updater.update_classifieds(category)

    db.close()
