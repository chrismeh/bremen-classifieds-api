from marshmallow import fields

from bremen_classifieds_api.bin.api.extensions import ma


class CategorySchema(ma.Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    slug = fields.String()
    title = fields.String()
    classified_count = fields.Integer()
    url = fields.String()

    _links = ma.Hyperlinks({"classifieds": ma.AbsoluteURLFor(
        "categories.get_classifieds_by_category",
        values=dict(category_id="<id>"))
    })


class ClassifiedsSchema(ma.Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    category = fields.Pluck(CategorySchema, "id")
    slug = fields.String()
    title = fields.String()
    date = fields.Date()
    url = fields.String()
    has_picture = fields.Boolean()
    is_commercial = fields.Boolean()
