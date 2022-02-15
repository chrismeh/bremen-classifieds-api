from typing import Iterable, List, Optional

import mysql.connector

from bremen_classifieds_api.classifieds.categories import Category
from bremen_classifieds_api.classifieds.classifieds import Classified


class ClassifiedRepository:
    def __init__(self, db: mysql.connector.MySQLConnection):
        self._db = db

    def find_all(self, category: Category) -> List[Classified]:
        query = """
            SELECT cat.type, cat.slug, c.* FROM classified c
            LEFT JOIN category cat ON cat.id = c.category_id
            WHERE c.category_id = %s
            ORDER BY c.external_id DESC;
        """

        with self._db.cursor() as cursor:
            cursor.execute(query, (category.id,))
            return [self._to_object(row) for row in cursor]

    def insert_many(self, category: Category, classifieds: Iterable[Classified]):
        query = """
            INSERT INTO classified (external_id, category_id, slug, title, url, has_picture, is_commercial, publish_date, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE 
                updated_at = NOW();
        """

        with self._db.cursor(prepared=True) as cursor:
            params = [self._to_database(category, classified) for classified in classifieds]
            cursor.executemany(query, params)

    def _to_database(self, category: Category, classified: Classified) -> tuple:
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

    def _to_object(self, row: tuple) -> Classified:
        cat_type, cat_slug, classified_id, _, slug, title, url, has_picture, is_commercial, publish_date, *_ = row
        return Classified(classified_id, cat_type, cat_slug, slug, title, publish_date, url, has_picture, is_commercial)


class CategoryRepository:
    def __init__(self, db: mysql.connector.MySQLConnection):
        self._db = db

    def find_all(self) -> List[Category]:
        query = "SELECT * FROM category;"

        with self._db.cursor() as cursor:
            cursor.execute(query)
            return [self._to_object(row) for row in cursor]

    def find_by_slug(self, category_type: str, slug: str) -> Optional[Category]:
        query = "SELECT * FROM category WHERE `type` = %s AND slug = %s LIMIT 1;"
        with self._db.cursor() as cursor:
            cursor.execute(query, (category_type, slug))
            if (row := cursor.fetchone()) is None:
                return None

            return self._to_object(row)

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
        category_id, category_type, slug, title, classified_count, url, *_ = row
        return Category(category_type, slug, title, classified_count, url, category_id)
