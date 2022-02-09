import dataclasses

import requests
from flask import jsonify, Blueprint, abort

import bremen_classifieds_api.classifieds as classifieds
from bremen_classifieds_api.extensions import cache

bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@bp.get("/")
def get_categories():
    client = classifieds.Client(requests.session())
    facade = classifieds.Facade(client, cache)

    categories = facade.get_categories()
    return jsonify([dataclasses.asdict(category) for category in categories])


@bp.get("/<category_type>/<slug>")
def get_classifieds(category_type: str, slug: str):
    client = classifieds.Client(requests.session())
    facade = classifieds.Facade(client, cache)

    classifieds_list = facade.get_classifieds_for_category(category_type, slug)
    if classifieds_list is None:
        abort(404)

    return jsonify([dataclasses.asdict(classified) for classified in classifieds_list])
