import re
from dataclasses import dataclass
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup


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
    soup = BeautifulSoup(html, "html.parser")
    classified = soup.select(".eintraege_list li a")[0]

    return [Classified(
        id=int(re.match(r".+?(\d+)\.html$", classified.attrs["href"]).group(1)),
        category_type=classified.attrs["href"].split("/")[1],
        category_slug=classified.attrs["href"].split("/")[2],
        slug=re.sub(r"-(\d+)\.html", "", classified.attrs["href"].split("/").pop()),
        title=re.sub(r" (?:\d{2}\.?){3}", "", ' '.join(classified.text.split())),
        date=datetime.strptime(classified.select_one(".list_date").text.strip(), "%d.%m.%y").date(),
        url="https://schwarzesbrett.bremen.de" + classified.attrs["href"],
        has_picture=classified.select_one(".fa-camera") is not None,
        is_commercial=classified.select_one(".fa-eur") is not None,
    )]
