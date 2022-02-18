from typing import Iterable

from bremen_classifieds_api.classifieds.categories import Category
from bremen_classifieds_api.classifieds.classifieds import Classified
from bremen_classifieds_api.classifieds.client import Client
from bremen_classifieds_api.classifieds.db import CategoryRepository, ClassifiedRepository


class Updater:
    def __init__(self, client: Client, category_repo: CategoryRepository, classified_repo: ClassifiedRepository):
        self._client = client
        self._category_repo = category_repo
        self._classified_repo = classified_repo

    def update_categories(self) -> Iterable[Category]:
        new_categories = self._client.get_categories()
        self._category_repo.insert_many(new_categories)
        return self._category_repo.find_all()

    def update_classifieds(self, category: Category) -> Iterable[Classified]:
        new_classifieds = self._client.get_classifieds(category)
        self._classified_repo.insert_many(category, new_classifieds)
        return self._classified_repo.find_all(category)
