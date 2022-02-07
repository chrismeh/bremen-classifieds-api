from typing import List

import requests

from bremen_classifieds_api.classifieds import Category, parse_categories


class Client:
    base_url = "https://schwarzesbrett.bremen.de/"

    def __init__(self, session: requests.Session):
        self.__session = session

    def get_categories(self) -> List[Category]:
        response = self.__session.get(self.base_url)
        return parse_categories(response.text)
