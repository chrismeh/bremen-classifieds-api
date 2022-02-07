import httpretty
import pytest
import requests

from bremen_classifieds_api.classifieds import Category, Client, HttpError
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
