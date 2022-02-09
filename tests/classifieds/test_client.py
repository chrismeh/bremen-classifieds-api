import httpretty
import pytest
import requests

from bremen_classifieds_api.classifieds.categories import Category
from bremen_classifieds_api.classifieds.classifieds import Classified
from bremen_classifieds_api.classifieds.client import Client, HttpError
from tests.classifieds.conftest import fixture


@httpretty.activate
def test_client_get_categories():
    httpretty.register_uri(
        method=httpretty.GET,
        uri=Client.base_url,
        status=200,
        body=fixture("single_category.html")
    )

    client = Client(requests.session())
    response = client.get_categories()

    assert type(response) is list
    assert len(response) == 1
    assert type(response.pop()) is Category


@httpretty.activate
def test_client_get_categories_with_http_error():
    httpretty.register_uri(
        method=httpretty.GET,
        uri=Client.base_url,
        status=500
    )

    client = Client(requests.session())

    with pytest.raises(HttpError) as err:
        client.get_categories()

    assert str(err.value) == f"expected http status code 200 for {Client.base_url}, got 500"


@httpretty.activate
def test_client_get_classifieds():
    category = Category(
        category_type="verkauf-angebote",
        slug="arbeitsplatzangebote-gemeinnuetzig",
        title="Jobangebote gemeinnütziger Einrichtungen",
        classified_count=218,
        url="https://schwarzesbrett.bremen.de/verkauf-angebote/rubrik/arbeitsplatzangebote-gemeinnuetzig.html"
    )

    httpretty.register_uri(
        method=httpretty.GET,
        uri=category.url,
        status=200,
        body=fixture("single_classified.html")
    )

    client = Client(requests.session())
    response = client.get_classifieds(category)

    assert type(response) is list
    assert len(response) == 1
    assert type(response.pop()) is Classified


@httpretty.activate
def test_client_get_classifieds_with_http_error():
    category = Category(
        category_type="verkauf-angebote",
        slug="arbeitsplatzangebote-gemeinnuetzig",
        title="Jobangebote gemeinnütziger Einrichtungen",
        classified_count=218,
        url="https://schwarzesbrett.bremen.de/verkauf-angebote/rubrik/arbeitsplatzangebote-gemeinnuetzig.html"
    )

    httpretty.register_uri(
        method=httpretty.GET,
        uri=category.url,
        status=500
    )

    client = Client(requests.session())

    with pytest.raises(HttpError) as err:
        client.get_classifieds(category)

    assert str(err.value) == f"expected http status code 200 for {category.url}, got 500"
