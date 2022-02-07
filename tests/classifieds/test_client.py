import httpretty
import requests

from bremen_classifieds_api.classifieds import Category, Client
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
