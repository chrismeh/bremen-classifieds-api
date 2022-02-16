import os
from unittest.mock import create_autospec

import pytest

from bremen_classifieds_api.classifieds.client import Client


def fixture(file_name: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), f"fixtures/{file_name}")) as f:
        return f.read()


@pytest.fixture
def client() -> Client:
    return create_autospec(Client)
