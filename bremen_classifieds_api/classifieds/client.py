from typing import List

import requests

from bremen_classifieds_api.classifieds import Category, parse_categories


class HttpError(Exception):
    pass


class Client:
    base_url = "https://schwarzesbrett.bremen.de/"

    def __init__(self, session: requests.Session):
        self.__session = session

    def get_categories(self) -> List[Category]:
        response = self.__session.get(self.base_url)
        if response.status_code != 200:
            raise HttpError(f"expected http status code 200 for {self.base_url}, got {response.status_code}")

        return parse_categories(response.text)
