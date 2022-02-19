import re
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from bremen_classifieds_api.classifieds.categories import Category


@dataclass
class Classified:
    id: int
    category: Category
    slug: str
    title: str
    date: datetime.date
    url: str
    has_picture: bool
    is_commercial: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class NewClassified:
    id: int
    slug: str
    title: str
    date: date
    url: str
    has_picture: bool = False
    is_commercial: bool = False


@dataclass
class Filter:
    search: Optional[str] = None
    has_picture: Optional[bool] = None
    is_commercial: Optional[bool] = None
    updated_since: Optional[datetime] = None


def parse_classifieds(html: str) -> List[NewClassified]:
    soup = BeautifulSoup(html, "html.parser")
    classifieds = soup.select(".eintraege_list li a")

    classifieds = [parse_classified(classified) for classified in classifieds]
    return list(filter(lambda c: c is not None, classifieds))


def parse_classified(soup: Tag) -> Optional[NewClassified]:
    try:
        return NewClassified(
            id=parse_classified_id(soup),
            slug=parse_classified_slug(soup),
            title=parse_classified_title(soup),
            date=parse_classified_date(soup),
            url="https://schwarzesbrett.bremen.de" + soup.attrs["href"],
            has_picture=parse_classified_picture_flag(soup),
            is_commercial=parse_classified_commercial_flag(soup),
        )
    except ValueError as err:
        print(f"error when parsing classified at {soup.attrs['href']}: {err}")
        return None


def parse_classified_id(soup: Tag) -> int:
    return int(re.match(r".+?(\d+)\.html$", soup.attrs["href"]).group(1))


def parse_classified_slug(soup: Tag) -> str:
    return re.sub(r"-(\d+)\.html", "", soup.attrs["href"].split("/").pop())


def parse_classified_title(soup: Tag) -> str:
    return re.sub(r" (?:\d{2}\.?){3}", "", ' '.join(soup.text.split()))


def parse_classified_date(soup: Tag) -> date:
    return datetime.strptime(soup.select_one(".list_date").text.strip(), "%d.%m.%y").date()


def parse_classified_picture_flag(soup: Tag) -> bool:
    return soup.select_one(".fa-camera") is not None


def parse_classified_commercial_flag(soup: Tag) -> bool:
    return soup.select_one(".fa-eur") is not None
