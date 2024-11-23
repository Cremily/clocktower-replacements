from bs4 import BeautifulSoup, ResultSet, NavigableString, Tag
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote
from typing import Any, List, TypedDict
import json
import time

soup = BeautifulSoup


base_url = "https://script.bloodontheclocktower.com"
chars_url = base_url + "/data/roles.json"


class Character(TypedDict):

    id: str
    name: str
    roleType: str
    print: str
    icon: str
    version: str


def get_chars(url=chars_url) -> List[Character]:

    chars = list(
        json.loads(str(soup(urlopen(url).read(), "html.parser"))),
    )
    fp = open("roles.json", "w+")
    json.dump(chars, fp)
    return chars


def save_icons(url=chars_url):
    chars = get_chars(url)
    for char in chars:
        char_url = base_url + quote(
            char["icon"][1:],
        )
 
        urlretrieve(char_url, "./icons/" + char["id"] + ".webp")


if __name__ == "__main__":
    save_icons()
