import dataclasses

import requests
from flask import Flask, jsonify, abort

from bremen_classifieds_api.classifieds import Client

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.get("/api/categories")
def get_categories():
    client = Client(requests.session())
    categories = client.get_categories()

    return jsonify([dataclasses.asdict(category) for category in categories])


@app.get("/api/categories/<category_type>/<slug>")
def get_classifieds(category_type: str, slug: str):
    client = Client(requests.session())
    categories = client.get_categories()
    category = next(filter(lambda c: c.category_type == category_type and c.slug == slug, categories), None)

    if category is None:
        abort(404)

    classifieds = client.get_classifieds(category)
    return jsonify([dataclasses.asdict(classified) for classified in classifieds])
