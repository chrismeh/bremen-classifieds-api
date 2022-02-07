from datetime import date

from bremen_classifieds_api.classifieds import Classified, parse_classifieds


def test_parse_classified_with_single_classified(html_for_single_classified):
    expected_classifieds = [
        Classified(
            id=20346305,
            category_type="verkauf-angebote",
            category_slug="arbeitsplatzangebote-verkauf",
            slug="lagerhelfer-mwd-in-tagschicht---in-habenhausen",
            title="Lagerhelfer (m/w/d) in Tagschicht - in Habenhausen",
            date=date(2022, 2, 7),
            url="https://schwarzesbrett.bremen.de/verkauf-angebote/arbeitsplatzangebote-verkauf/lagerhelfer-mwd-in-tagschicht---in-habenhausen-20346305.html",
            is_commercial=True
        )
    ]

    assert parse_classifieds(html_for_single_classified) == expected_classifieds