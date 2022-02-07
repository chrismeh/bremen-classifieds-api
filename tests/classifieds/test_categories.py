from bremen_classifieds_api.classifieds.categories import Category, parse_categories


def test_parse_categories_with_single_category(html_for_single_category):
    expected_categories = [
        Category(
            category_type="verkauf-angebote",
            slug="arbeitsplatzangebote-gemeinnuetzig",
            title="Jobangebote gemeinnütziger Einrichtungen",
            classified_count=218,
            url="https://schwarzesbrett.bremen.de/verkauf-angebote/rubrik/arbeitsplatzangebote-gemeinnuetzig.html"
        )
    ]

    assert parse_categories(html_for_single_category) == expected_categories
