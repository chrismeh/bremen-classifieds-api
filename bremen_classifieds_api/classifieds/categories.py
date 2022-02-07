from dataclasses import dataclass
from typing import List


@dataclass
class Category:
    category_type: str
    slug: str
    title: str
    classified_count: int
    url: str


def parse_categories(html: str) -> List[Category]:
    pass
