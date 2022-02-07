import re
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup, Tag


@dataclass
class Category:
    category_type: str
    slug: str
    title: str
    classified_count: int
    url: str


def parse_categories(html: str) -> List[Category]:
    soup = BeautifulSoup(html, "html.parser")
    categories = soup.select(".rubriken_list li a")

    return [parse_category(category) for category in categories]


def parse_category(soup: Tag) -> Category:
    return Category(
        category_type=soup.attrs["href"].split("/")[1],
        slug=soup.attrs["href"].split("/").pop().replace(".html", ""),
        title=re.sub(r" \d*$", "", ' '.join(soup.text.split())),
        classified_count=int(soup.select_one(".rubriken_count").text),
        url="https://schwarzesbrett.bremen.de" + soup.attrs["href"],
    )
