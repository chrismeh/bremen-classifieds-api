import os

import pytest


def fixture(file_name: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), f"fixtures/{file_name}")) as f:
        return f.read()


@pytest.fixture
def html_for_single_category() -> str:
    return fixture("single_category.html")


@pytest.fixture
def html_for_multiple_categories() -> str:
    return fixture("multiple_categories.html")


@pytest.fixture
def html_for_single_classified() -> str:
    return fixture("single_classified.html")


@pytest.fixture
def html_for_single_classified_with_picture() -> str:
    return fixture("single_classified_with_picture.html")


@pytest.fixture
def html_for_single_classified_non_commercial() -> str:
    return fixture("single_classified_non_commercial.html")


@pytest.fixture
def html_for_multiple_classifieds() -> str:
    return fixture("multiple_classifieds.html")
