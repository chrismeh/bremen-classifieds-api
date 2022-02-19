from datetime import datetime
from typing import Optional, Callable

from flask import jsonify, Blueprint, request

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
    try:
        classified_filter = parse_classifieds_filter()
    except ValueError as err:
        print(err)
        return jsonify(error="Bad Request"), 400

    category_repo = CategoryRepository(db.connection)
    classifieds_repo = ClassifiedRepository(db.connection)

    category = category_repo.find_by_id(category_id)
    if category is None:
        return jsonify(error="Not Found"), 404

    classifieds_list = classifieds_repo.find_all(category, classified_filter)
    return jsonify(ClassifiedsSchema(many=True).dump(classifieds_list))


def parse_classifieds_filter() -> Filter:
    def parse_request_arg(arg: str, key: Optional[Callable] = None):
        if (value := request.args.get(arg)) is None:
            return None
        return value if key is None else key(value)

    f = Filter(
        search=parse_request_arg("search"),
        has_picture=parse_request_arg("has_picture", lambda x: x == "1"),
        is_commercial=parse_request_arg("is_commercial", lambda x: x == "1"),
        updated_since=parse_request_arg("updated_since", lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")),
    )

    return f
