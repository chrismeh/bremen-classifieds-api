from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Classified:
    id: int
    category_type: str
    category_slug: str
    slug: str
    title: str
    date: datetime.date
    url: str
    has_picture: bool = False
    is_commercial: bool = False


def parse_classifieds(html: str) -> List[Classified]:
    pass
