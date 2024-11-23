import json
import typing
from replacements import REPLACEMENTS
from get_characters import Character


class Script(typing.TypedDict):

    name: str
    author: str
    characters: list[str]


def read_script(script_path: str) -> Script:
    fp = open(script_path)
    script = json.load(fp)
    meta = {}
    characters = []
    for i, value in enumerate(script):
        if i == 0:
            meta = value
        else:
            characters.append(value)
    return {"name": meta["name"], "author": meta["author"], "characters": characters}


def _get_valid_replacement(
    replacement: str, possibles: list[str], used_replacements: list[str]
):
    for possible in possibles:
        if possible not in used_replacements:
            print(possible, possibles, used_replacements)
            return possible
    return None


def get_replacements(
    script: Script, _replacements: dict[str, list[str]] = REPLACEMENTS
):
    replacements = {}
    used_replacements = [i for i in script["characters"]]
    for replacement in _replacements:
        if replacement in script["characters"]:
            valid_rep = _get_valid_replacement(
                replacement,
                REPLACEMENTS[replacement],
                used_replacements,
            )
            replacements[replacement] = valid_rep
            if valid_rep is not None:
                used_replacements.append(valid_rep)
    return replacements
