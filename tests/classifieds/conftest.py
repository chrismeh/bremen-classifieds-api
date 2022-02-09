import os
from unittest.mock import create_autospec

import pytest
from flask_caching import Cache

from bremen_classifieds_api.classifieds import Client


def fixture(file_name: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), f"fixtures/{file_name}")) as f:
        return f.read()


@pytest.fixture
def cache() -> Cache:
    return create_autospec(Cache)


@pytest.fixture
def client() -> Client:
    return create_autospec(Client)
