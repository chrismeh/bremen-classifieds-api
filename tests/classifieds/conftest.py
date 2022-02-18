import os
from unittest.mock import create_autospec

import pytest

from bremen_classifieds_api.classifieds.client import Client
from bremen_classifieds_api.classifieds.db import CategoryRepository, ClassifiedRepository


def fixture(file_name: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), f"fixtures/{file_name}")) as f:
        return f.read()


@pytest.fixture
def client() -> Client:
    return create_autospec(Client)


@pytest.fixture
def category_repository() -> CategoryRepository:
    return create_autospec(CategoryRepository)


@pytest.fixture
def classified_repository() -> ClassifiedRepository:
    return create_autospec(ClassifiedRepository)
