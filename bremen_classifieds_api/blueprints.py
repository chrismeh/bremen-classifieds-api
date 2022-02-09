import dataclasses

import requests
from flask import jsonify, abort, Blueprint

from bremen_classifieds_api.classifieds import Client
from bremen_classifieds_api.extensions import cache

bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@bp.get("/")
def get_categories():
    client = Client(requests.session())

    cache_key = "categories"
    categories = cache.get(cache_key)
    if categories is None:
        categories = client.get_categories()
        cache.set(cache_key, categories)

    return jsonify([dataclasses.asdict(category) for category in categories])


@bp.get("/<category_type>/<slug>")
def get_classifieds(category_type: str, slug: str):
    client = Client(requests.session())

    classifieds_cache_key = f"category-{category_type}-{slug}"
    classifieds = cache.get(classifieds_cache_key)
    if classifieds is not None:
        return jsonify([dataclasses.asdict(classified) for classified in classifieds])

    category_cache_key = "categories"
    categories = cache.get(category_cache_key)
    if categories is None:
        categories = client.get_categories()
        cache.set(category_cache_key, categories)

    category = next(filter(lambda c: c.category_type == category_type and c.slug == slug, categories), None)
    if category is None:
        abort(404)

    classifieds = client.get_classifieds(category)
    cache.set(classifieds_cache_key, classifieds)

    return jsonify([dataclasses.asdict(classified) for classified in classifieds])
