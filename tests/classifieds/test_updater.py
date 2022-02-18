import datetime

from bremen_classifieds_api.classifieds.categories import NewCategory, Category
from bremen_classifieds_api.classifieds.classifieds import NewClassified
from bremen_classifieds_api.classifieds.updater import Updater


def test_updater_update_categories(client, category_repository, classified_repository):
    new_categories = [NewCategory(category_type="foo", slug="bar-baz", title="Test", classified_count=1337, url="/")]
    client.get_categories.return_value = new_categories

    updater = Updater(client, category_repository, classified_repository)
    updater.update_categories()

    category_repository.insert_many.assert_called_with(new_categories)


def test_updater_update_classifieds(client, category_repository, classified_repository):
    category = Category(
        id=1,
        category_type="foo",
        slug="bar-baz",
        title="Test",
        classified_count=1337,
        url="/",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    new_classifieds = [NewClassified(42, "foo-bar", "baz", datetime.datetime.now(), url="/")]
    client.get_classifieds.return_value = new_classifieds

    updater = Updater(client, category_repository, classified_repository)
    updater.update_classifieds(category)

    classified_repository.insert_many.assert_called_with(category, new_classifieds)
