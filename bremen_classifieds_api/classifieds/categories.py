import re
from dataclasses import dataclass
from typing import List, Optional

from bs4 import BeautifulSoup, Tag


@dataclass
class Category:
    category_type: str
    slug: str
    title: str
    classified_count: int
    url: str
    id: Optional[int] = None


def parse_categories(html: str) -> List[Category]:
    soup = BeautifulSoup(html, "html.parser")
    categories = soup.select(".rubriken_list li a")

    return [parse_category(category) for category in categories]


def parse_category(soup: Tag) -> Category:
    return Category(
        category_type=parse_category_type(soup),
        slug=parse_category_slug(soup),
        title=parse_category_title(soup),
        classified_count=parse_category_classifieds_count(soup),
        url="https://schwarzesbrett.bremen.de" + soup.attrs["href"],
    )


def parse_category_type(soup: Tag) -> str:
    return soup.attrs["href"].split("/")[1]


def parse_category_slug(soup: Tag) -> str:
    return soup.attrs["href"].split("/").pop().replace(".html", "")


def parse_category_title(soup: Tag) -> str:
    return re.sub(r" \d*$", "", ' '.join(soup.text.split()))


def parse_category_classifieds_count(soup: Tag) -> int:
    return int(soup.select_one(".rubriken_count").text)
