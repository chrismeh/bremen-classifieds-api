from marshmallow import fields

from bremen_classifieds_api.extensions import ma


class CategorySchema(ma.Schema):
    class Meta:
        ordered = True

    category_type = fields.String()
    slug = fields.String()
    title = fields.String()
    classified_count = fields.Integer()
    url = fields.String()

    _links = ma.Hyperlinks({"classifieds": ma.AbsoluteURLFor(
        "categories.get_classifieds_by_category",
        values=dict(category_type="<category_type>", slug="<slug>"))
    })


class ClassifiedsSchema(ma.Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    category_type = fields.String()
    category_slug = fields.String()
    slug = fields.String()
    title = fields.String()
    date = fields.Date()
    url = fields.String()
    has_picture = fields.Boolean()
    is_commercial = fields.Boolean()

    _links = ma.Hyperlinks({"self": ma.AbsoluteURLFor(
        "categories.get_classifieds_by_category",
        values=dict(category_type="<category_type>", slug="<category_slug>"))
    })
