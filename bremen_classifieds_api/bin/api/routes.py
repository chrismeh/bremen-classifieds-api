from flask import jsonify, Blueprint, abort, request

from bremen_classifieds_api.bin.api.extensions import db
from bremen_classifieds_api.bin.api.schemas import CategorySchema, ClassifiedsSchema
from bremen_classifieds_api.classifieds.classifieds import Filter
from bremen_classifieds_api.classifieds.db import CategoryRepository, ClassifiedRepository

bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@bp.get("/")
def get_categories():
    repo = CategoryRepository(db.connection)

    categories = repo.find_all()
    return jsonify(CategorySchema(many=True).dump(categories))


@bp.get("/<int:category_id>")
def get_classifieds_by_category(category_id: int):
    category_repo = CategoryRepository(db.connection)
    classifieds_repo = ClassifiedRepository(db.connection)

    category = category_repo.find_by_id(category_id)
    if category is None:
        abort(404)

    classifieds_list = classifieds_repo.find_all(category, parse_classifieds_filter())
    return jsonify(ClassifiedsSchema(many=True).dump(classifieds_list))


def parse_classifieds_filter() -> Filter:
    f = Filter()
    if (search := request.args.get("search")) is not None:
        f.search = search

    if (has_picture := request.args.get("has_picture")) is not None:
        f.has_picture = has_picture == "1"

    if (is_commercial := request.args.get("is_commercial")) is not None:
        f.is_commercial = is_commercial == "1"

    return f
