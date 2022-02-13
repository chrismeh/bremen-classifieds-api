import requests
from flask import jsonify, Blueprint, abort

import bremen_classifieds_api.classifieds as classifieds
from bremen_classifieds_api.extensions import cache
from bremen_classifieds_api.schemas import CategorySchema, ClassifiedsSchema

bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@bp.get("/")
def get_categories():
    client = classifieds.Client(requests.session())
    facade = classifieds.Facade(client, cache)

    return jsonify(CategorySchema(many=True).dump(facade.get_categories()))


@bp.get("/<category_type>/<slug>")
def get_classifieds_by_category(category_type: str, slug: str):
    client = classifieds.Client(requests.session())
    facade = classifieds.Facade(client, cache)

    classifieds_list = facade.get_classifieds_for_category(category_type, slug)
    if classifieds_list is None:
        abort(404)

    return jsonify(ClassifiedsSchema(many=True).dump(classifieds_list))
