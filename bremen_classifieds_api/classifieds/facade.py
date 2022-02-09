from typing import Protocol, List, Optional

from bremen_classifieds_api.classifieds.categories import Category
from bremen_classifieds_api.classifieds.classifieds import Classified
from bremen_classifieds_api.classifieds.client import Client


class Cache(Protocol):
    def get(self, *args, **kwargs) -> bool:
        pass

    def set(self, *args, **kwargs) -> bool:
        pass


class Facade:
    category_cache_key = "categories"

    def __init__(self, client: Client, cache: Cache):
        self._client = client
        self._cache = cache

    def get_categories(self) -> List[Category]:
        categories = self._cache.get(self.category_cache_key)
        if categories is None:
            categories = self._client.get_categories()
            self._cache.set(self.category_cache_key, categories)

        return categories

    def get_classifieds_for_category(self, category_type: str, slug: str) -> Optional[List[Classified]]:
        categories = self.get_categories()
        wanted_category = next(filter(lambda c: c.category_type == category_type and c.slug == slug, categories), None)
        if wanted_category is None:
            return None

        classified_cache_key = self._build_classified_cache_key(wanted_category)
        classifieds = self._cache.get(classified_cache_key)
        if classifieds is None:
            classifieds = self._client.get_classifieds(wanted_category)
            self._cache.set(classified_cache_key, classifieds)

        return classifieds

    def _build_classified_cache_key(self, category: Category) -> str:
        return f"classifieds-{category.category_type}-{category.slug}"
