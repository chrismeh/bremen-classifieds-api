from datetime import date

from bremen_classifieds_api.classifieds.classifieds import parse_classifieds, NewClassified
from tests.classifieds.conftest import fixture


def test_parse_classified_with_single_classified():
    expected_classifieds = [
        NewClassified(
            id=20346305,
            slug="lagerhelfer-mwd-in-tagschicht---in-habenhausen",
            title="Lagerhelfer (m/w/d) in Tagschicht - in Habenhausen",
            date=date(2022, 2, 7),
            url="https://schwarzesbrett.bremen.de/verkauf-angebote/arbeitsplatzangebote-verkauf/lagerhelfer-mwd-in-tagschicht---in-habenhausen-20346305.html",
            is_commercial=True
        )
    ]

    assert parse_classifieds(fixture("single_classified.html")) == expected_classifieds


def test_parse_classified_with_classified_with_picture():
    classifieds = parse_classifieds(fixture("single_classified_with_picture.html"))

    assert classifieds[0].has_picture is True


def test_parse_classified_with_classified_non_commercial():
    classifieds = parse_classifieds(fixture("single_classified_non_commercial.html"))

    assert classifieds[0].is_commercial is False


def test_parse_classified_with_multiple_classifieds():
    expected_classifieds = [
        NewClassified(
            id=20346305,
            slug="lagerhelfer-mwd-in-tagschicht---in-habenhausen",
            title="Lagerhelfer (m/w/d) in Tagschicht - in Habenhausen",
            date=date(2022, 2, 7),
            url="https://schwarzesbrett.bremen.de/verkauf-angebote/arbeitsplatzangebote-verkauf/lagerhelfer-mwd-in-tagschicht---in-habenhausen-20346305.html",
            is_commercial=True
        ),
        NewClassified(
            id=20367236,
            slug="gabelstaplerfahrer-mwd-in-bremen",
            title="Gabelstaplerfahrer (m/w/d) in Bremen",
            date=date(2022, 2, 7),
            url="https://schwarzesbrett.bremen.de/verkauf-angebote/arbeitsplatzangebote-verkauf/gabelstaplerfahrer-mwd-in-bremen-20367236.html",
            is_commercial=True
        ),
        NewClassified(
            id=20346302,
            slug="staplerfahrer-mwd-in-heeslingen",
            title="Staplerfahrer (m/w/d) in Heeslingen",
            date=date(2022, 2, 7),
            url="https://schwarzesbrett.bremen.de/verkauf-angebote/arbeitsplatzangebote-verkauf/staplerfahrer-mwd-in-heeslingen-20346302.html",
            is_commercial=True
        ),

    ]

    assert parse_classifieds(fixture("multiple_classifieds.html")) == expected_classifieds
