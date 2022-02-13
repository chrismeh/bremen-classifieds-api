import re
from typing import Protocol, List, Optional

from bremen_classifieds_api.classifieds.categories import Category
from bremen_classifieds_api.classifieds.classifieds import Classified, Filter
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

    def get_classifieds_for_category(self, category_type: str, slug: str,
                                     classified_filter: Filter = Filter()) -> Optional[List[Classified]]:
        categories = self.get_categories()
        wanted_category = next(filter(lambda c: c.category_type == category_type and c.slug == slug, categories), None)
        if wanted_category is None:
            return None

        classified_cache_key = self._build_classified_cache_key(wanted_category)
        classifieds = self._cache.get(classified_cache_key)
        if classifieds is None:
            classifieds = self._client.get_classifieds(wanted_category)
            self._cache.set(classified_cache_key, classifieds)

        return self._filter_classifieds(classifieds, classified_filter)

    def _filter_classifieds(self, classifieds: List[Classified], classified_filter: Filter) -> List[Classified]:
        def title_matcher(c: Classified):
            return re.search(re.escape(classified_filter.search), c.title, flags=re.IGNORECASE)

        def picture_matcher(c: Classified):
            return c.has_picture == classified_filter.has_picture

        def commercial_matcher(c: Classified):
            return c.is_commercial == classified_filter.is_commercial

        filters = []
        if classified_filter.search is not None:
            filters.append(title_matcher)
        if classified_filter.has_picture is not None:
            filters.append(picture_matcher)
        if classified_filter.is_commercial is not None:
            filters.append(commercial_matcher)

        return list(filter(lambda x: all(f(x) for f in filters), classifieds))

    def _build_classified_cache_key(self, category: Category) -> str:
        return f"classifieds-{category.category_type}-{category.slug}"
