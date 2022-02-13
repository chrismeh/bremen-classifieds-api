import datetime

from bremen_classifieds_api.classifieds import Facade
from bremen_classifieds_api.classifieds.categories import Category
from bremen_classifieds_api.classifieds.classifieds import Classified, Filter


def test_get_categories_return_categories_on_cache_hit(client, cache):
    cached_value = [Category("foo", "bar", "baz", 100, "qux")]
    cache.get.return_value = cached_value

    facade = Facade(client, cache)
    assert facade.get_categories() == cached_value


def test_get_categories_return_categories_on_cache_miss(client, cache):
    client_response = [Category("foo", "bar", "baz", 100, "qux")]
    cache.get.return_value = None
    client.get_categories.return_value = client_response

    facade = Facade(client, cache)
    assert facade.get_categories() == client_response
    cache.set.assert_called_once()


def test_get_classifieds_for_category_return_none_if_category_could_not_be_matched(client, cache):
    cached_value = [Category("foo", "bar", "baz", 100, "qux")]
    cache.get.return_value = cached_value

    facade = Facade(client, cache)
    assert facade.get_classifieds_for_category("not", "found") is None


def test_get_classifieds_for_category_return_classifieds_on_cache_hit(client, cache):
    cached_category_value = [Category("foo", "bar", "baz", 100, "qux")]
    cached_classifieds_value = [Classified(1, "foo", "bar", "baz", "qux", datetime.date.today(), "/", True, True)]

    cache.get.side_effect = [cached_category_value, cached_classifieds_value]

    facade = Facade(client, cache)
    assert facade.get_classifieds_for_category("foo", "bar") == cached_classifieds_value


def test_get_classifieds_for_category_return_classifieds_on_cache_miss(client, cache):
    cached_category_value = [Category("foo", "bar", "baz", 100, "qux")]
    client_response = [Classified(1, "foo", "bar", "baz", "qux", datetime.date.today(), "/", True, True)]

    cache.get.side_effect = [cached_category_value, None]
    client.get_classifieds.return_value = client_response

    facade = Facade(client, cache)
    assert facade.get_classifieds_for_category("foo", "bar") == client_response
    cache.set.assert_called_once()


def test_get_classifieds_for_category_return_filtered_classifieds_for_search_term_match(client, cache):
    cached_category_value = [Category("foo", "bar", "baz", 100, "qux")]
    cached_classifieds_value = [
        Classified(1, "category_type", "category_type", "slug", "first classified", datetime.date.today(), "/"),
        Classified(2, "category_type", "category_type", "slug", "second classified", datetime.date.today(), "/")
    ]

    cache.get.side_effect = [cached_category_value, cached_classifieds_value]

    facade = Facade(client, cache)
    classifieds = facade.get_classifieds_for_category("foo", "bar", Filter(search="second"))

    assert len(classifieds) == 1
    assert classifieds[0] == cached_classifieds_value[1]


def test_get_classifieds_for_category_return_empty_list_for_non_matching_filter(client, cache):
    cached_category_value = [Category("foo", "bar", "baz", 100, "qux")]
    cached_classifieds_value = [
        Classified(1, "category_type", "category_type", "slug", "first classified", datetime.date.today(), "/"),
        Classified(2, "category_type", "category_type", "slug", "second classified", datetime.date.today(), "/")
    ]

    cache.get.side_effect = [cached_category_value, cached_classifieds_value]

    facade = Facade(client, cache)
    classifieds = facade.get_classifieds_for_category("foo", "bar", Filter(search="third"))

    assert len(classifieds) == 0


def test_get_classifieds_for_category_return_filtered_classifieds_for_picture_match(client, cache):
    cached_category_value = [Category("foo", "bar", "baz", 100, "qux")]
    cached_classifieds_value = [
        Classified(1, "category_type", "category_type", "slug", "first classified", datetime.date.today(), "/", True),
        Classified(2, "category_type", "category_type", "slug", "second classified", datetime.date.today(), "/")
    ]

    cache.get.side_effect = [cached_category_value, cached_classifieds_value]

    facade = Facade(client, cache)
    classifieds = facade.get_classifieds_for_category("foo", "bar", Filter(has_picture=True))

    assert len(classifieds) == 1
    assert classifieds[0] == cached_classifieds_value[0]


def test_get_classifieds_for_category_return_filtered_classifieds_for_commercial_match(client, cache):
    cached_category_value = [Category("foo", "bar", "baz", 100, "qux")]
    cached_classifieds_value = [
        Classified(1, "category_type", "category_type", "slug", "first classified", datetime.date.today(), "/"),
        Classified(2, "category_type", "category_type", "slug", "second classified", datetime.date.today(), "/", False,
                   True)
    ]

    cache.get.side_effect = [cached_category_value, cached_classifieds_value]

    facade = Facade(client, cache)
    classifieds = facade.get_classifieds_for_category("foo", "bar", Filter(is_commercial=True))

    assert len(classifieds) == 1
    assert classifieds[0] == cached_classifieds_value[1]
