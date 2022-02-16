from bremen_classifieds_api.classifieds.categories import parse_categories, NewCategory
from tests.classifieds.conftest import fixture


def test_parse_categories_with_single_category():
    expected_categories = [
        NewCategory(
            category_type="verkauf-angebote",
            slug="arbeitsplatzangebote-gemeinnuetzig",
            title="Jobangebote gemeinnütziger Einrichtungen",
            classified_count=218,
            url="https://schwarzesbrett.bremen.de/verkauf-angebote/rubrik/arbeitsplatzangebote-gemeinnuetzig.html"
        )
    ]

    assert parse_categories(fixture("single_category.html")) == expected_categories


def test_parse_categories_with_multiple_categories():
    expected_categories = [
        NewCategory(
            category_type="verkauf-angebote",
            slug="arbeitsplatzangebote-gemeinnuetzig",
            title="Jobangebote gemeinnütziger Einrichtungen",
            classified_count=218,
            url="https://schwarzesbrett.bremen.de/verkauf-angebote/rubrik/arbeitsplatzangebote-gemeinnuetzig.html"
        ),
        NewCategory(
            category_type="kauf-gesuche",
            slug="arbeitsplatzgesuche-kauf",
            title="Arbeitsplatzgesuche",
            classified_count=82,
            url="https://schwarzesbrett.bremen.de/kauf-gesuche/rubrik/arbeitsplatzgesuche-kauf.html"
        ),
        NewCategory(
            category_type="diverses",
            slug="gemeinschaftliches-wohnen",
            title="Bau- und Mietgemeinschaftsprojekte",
            classified_count=5,
            url="https://schwarzesbrett.bremen.de/diverses/rubrik/gemeinschaftliches-wohnen.html"
        ),
    ]

    assert parse_categories(fixture("multiple_categories.html")) == expected_categories
