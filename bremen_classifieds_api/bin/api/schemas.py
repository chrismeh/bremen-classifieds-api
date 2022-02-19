from marshmallow import fields

from bremen_classifieds_api.bin.api.extensions import ma


class CategorySchema(ma.Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    category_type = fields.String(data_key="type")
    slug = fields.String()
    title = fields.String()
    classified_count = fields.Integer()
    url = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    _links = ma.Hyperlinks({"classifieds": ma.AbsoluteURLFor(
        "categories.get_classifieds_by_category",
        values=dict(category_id="<id>"))
    })


class ClassifiedsSchema(ma.Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    category = fields.Nested(CategorySchema, only=["id", "category_type", "title"])
    slug = fields.String()
    title = fields.String()
    date = fields.Date()
    url = fields.String()
    has_picture = fields.Boolean()
    is_commercial = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
