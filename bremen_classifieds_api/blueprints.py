from flask import jsonify, Blueprint, abort, request

from bremen_classifieds_api.classifieds.classifieds import Filter
from bremen_classifieds_api.classifieds.db import CategoryRepository, ClassifiedRepository
from bremen_classifieds_api.extensions import db
from bremen_classifieds_api.schemas import CategorySchema, ClassifiedsSchema

bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@bp.get("/")
def get_categories():
    repo = CategoryRepository(db.connection)
    categories = repo.find_all()

    return jsonify(CategorySchema(many=True).dump(categories))


@bp.get("/<category_type>/<slug>")
def get_classifieds_by_category(category_type: str, slug: str):
    category_repo = CategoryRepository(db.connection)
    classifieds_repo = ClassifiedRepository(db.connection)

    category = category_repo.find_by_slug(category_type, slug)
    if category is None:
        abort(404)

    # TODO: Make me filterable again!
    classifieds_list = classifieds_repo.find_all(category)
    return jsonify(ClassifiedsSchema(many=True).dump(classifieds_list))


def parse_classifieds_filter() -> Filter:
    f = Filter()
    if (search := request.args.get("search", None)) is not None:
        f.search = search

    if (has_picture := request.args.get("has_picture", None)) is not None:
        f.has_picture = has_picture == "1"

    if (is_commercial := request.args.get("is_commercial", None)) is not None:
        f.is_commercial = is_commercial == "1"

    return f
