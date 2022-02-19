from typing import Iterable, List, Optional, Callable

import mysql.connector

from bremen_classifieds_api.classifieds.categories import Category, NewCategory
from bremen_classifieds_api.classifieds.classifieds import Classified, NewClassified, Filter


class ClassifiedRepository:
    def __init__(self, db: mysql.connector.MySQLConnection):
        self._db = db

    def find_all(self, category: Category, classified_filter: Optional[Filter] = None) -> List[Classified]:
        query, params = self._build_find_all_query(category, classified_filter)

        with self._db.cursor(prepared=True) as cursor:
            cursor.execute(query, params)
            return [ClassifiedMapper.to_object(row) for row in cursor]

    def insert_many(self, category: Category, classifieds: Iterable[NewClassified]):
        query = """
            INSERT INTO classified (external_id, category_id, slug, title, url, has_picture, is_commercial, publish_date, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE 
                updated_at = NOW();
        """

        with self._db.cursor(prepared=True) as cursor:
            params = [ClassifiedMapper.to_database(category, classified) for classified in classifieds]
            cursor.executemany(query, params)

    def _build_find_all_query(self, category: Category, classified_filter: Optional[Filter]) -> tuple:
        conditions = ["c.category_id = %s"]
        params = [category.id]

        if classified_filter is None:
            classified_filter = Filter()

        def handle_filter(value, condition: str, key: Optional[Callable] = None):
            if value is None:
                return
            conditions.append(condition)
            params.append(value if key is None else key(value))

        handle_filter(classified_filter.search, "c.title LIKE CONCAT('%', %s, '%')")
        handle_filter(classified_filter.has_picture, "c.has_picture = %s")
        handle_filter(classified_filter.is_commercial, "c.is_commercial = %s")
        handle_filter(classified_filter.updated_since, "c.updated_at >= %s", lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))

        where_string = " AND ".join(conditions)
        params = tuple(params)

        query = f"""
            SELECT cat.*, c.* FROM classified c
            LEFT JOIN category cat ON cat.id = c.category_id
            WHERE {where_string}
            ORDER BY c.external_id DESC;
        """

        return query, params


class ClassifiedMapper:
    @staticmethod
    def to_database(category: Category, classified: NewClassified) -> tuple:
        return (
            classified.id,
            category.id,
            classified.slug,
            classified.title,
            classified.url,
            classified.has_picture,
            classified.is_commercial,
            classified.date
        )

    @staticmethod
    def to_object(row: tuple) -> Classified:
        category_data, classified_data = row[:8], row[8:]
        category = CategoryMapper.to_object(category_data)

        classified_id, _, slug, title, url, has_picture, is_commercial, publish_date, created_at, updated_at = classified_data
        return Classified(classified_id, category, slug, title, publish_date, url, has_picture, is_commercial,
                          created_at, updated_at)


class CategoryRepository:
    def __init__(self, db: mysql.connector.MySQLConnection):
        self._db = db

    def find_all(self) -> List[Category]:
        query = "SELECT * FROM category;"

        with self._db.cursor(prepared=True) as cursor:
            cursor.execute(query)
            return [CategoryMapper.to_object(row) for row in cursor]

    def find_by_id(self, category_id: int) -> Optional[Category]:
        query = "SELECT * FROM category WHERE `id` = %s LIMIT 1;"
        with self._db.cursor(prepared=True) as cursor:
            cursor.execute(query, (category_id,))
            if (row := cursor.fetchone()) is None:
                return None

            return CategoryMapper.to_object(row)

    def insert_many(self, categories: Iterable[NewCategory]):
        query = """
            INSERT INTO category (type, slug, title, classified_count, url, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE
                classified_count = VALUES(classified_count),
                updated_at = NOW();
        """

        with self._db.cursor(prepared=True) as cursor:
            params = [CategoryMapper.to_database(category) for category in categories]
            cursor.executemany(query, params)


class CategoryMapper:
    @staticmethod
    def to_database(category: NewCategory) -> tuple:
        return category.category_type, category.slug, category.title, category.classified_count, category.url

    @staticmethod
    def to_object(row: tuple) -> Category:
        category_id, category_type, slug, title, classified_count, url, created_at, updated_at = row
        return Category(category_id, category_type, slug, title, classified_count, url, created_at, updated_at)
