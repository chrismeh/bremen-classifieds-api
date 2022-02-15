from typing import Iterable, List

import mysql.connector

from bremen_classifieds_api.classifieds.categories import Category


class CategoryRepository:
    def __init__(self, db: mysql.connector.MySQLConnection):
        self._db = db

    def find_all(self) -> List[Category]:
        query = "SELECT * FROM category;"

        with self._db.cursor() as cursor:
            cursor.execute(query)
            return [self._to_object(row) for row in cursor]

    def insert_many(self, categories: Iterable[Category]):
        query = """
            INSERT INTO category (type, slug, title, classified_count, url, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE
                classified_count = VALUES(classified_count),
                updated_at = NOW();
        """

        with self._db.cursor(prepared=True) as cursor:
            params = [self._to_database(category) for category in categories]
            cursor.executemany(query, params)

    def _to_database(self, category: Category) -> tuple:
        return category.category_type, category.slug, category.title, category.classified_count, category.url

    def _to_object(self, row: tuple) -> Category:
        _, category_type, slug, title, classified_count, url, *_ = row
        return Category(category_type, slug, title, classified_count, url)
