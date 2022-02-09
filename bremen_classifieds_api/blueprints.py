import dataclasses

import requests
from flask import jsonify, abort, Blueprint

from bremen_classifieds_api.classifieds import Client

bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@bp.get("/")
def get_categories():
    client = Client(requests.session())
    categories = client.get_categories()

    return jsonify([dataclasses.asdict(category) for category in categories])


@bp.get("/<category_type>/<slug>")
def get_classifieds(category_type: str, slug: str):
    client = Client(requests.session())
    categories = client.get_categories()
    category = next(filter(lambda c: c.category_type == category_type and c.slug == slug, categories), None)

    if category is None:
        abort(404)

    classifieds = client.get_classifieds(category)
    return jsonify([dataclasses.asdict(classified) for classified in classifieds])
