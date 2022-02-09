import dataclasses

import requests
from flask import jsonify, Blueprint, abort

from bremen_classifieds_api.classifieds import Client
from bremen_classifieds_api.classifieds.facade import Facade as ClassifiedsFacade
from bremen_classifieds_api.extensions import cache

bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@bp.get("/")
def get_categories():
    client = Client(requests.session())
    facade = ClassifiedsFacade(client, cache)

    categories = facade.get_categories()
    return jsonify([dataclasses.asdict(category) for category in categories])


@bp.get("/<category_type>/<slug>")
def get_classifieds(category_type: str, slug: str):
    client = Client(requests.session())
    facade = ClassifiedsFacade(client, cache)

    classifieds = facade.get_classifieds_for_category(category_type, slug)
    if classifieds is None:
        abort(404)

    return jsonify([dataclasses.asdict(classified) for classified in classifieds])
