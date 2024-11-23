from PIL import Image
import os
from script import get_replacements, read_script, Script
from get_characters import Character
import subprocess
from constants import CHARACTERS
from replacements import REPLACEMENTS
ICON_SIZE = 45
INITIAL_Y_OFFSET = 180
INITIAL_X_OFFSET = 5
CHARACTER_OFFSET = 101

OUTSIDER_OFFSET = 80
MINION_OFFSET = 70
DEMON_OFFSET = 60


def calc_character_counts(script: Script):
    counts = {"townsfolk": 0, "outsider": 0, "minion": 0, "demon": 0}
    for char in script["characters"]:
        matching_char: Character = next(x for x in CHARACTERS if x["id"] == char)
        try:
            counts[matching_char["roleType"]] += 1
        except KeyError:
            pass
    return counts


def calc_char_offset(i: int, counts: dict[str, int]) -> int:

    offset = (i) * CHARACTER_OFFSET
    if i > counts["townsfolk"] - 1:
        offset += OUTSIDER_OFFSET
    if i > counts["townsfolk"] + counts["outsider"] - 1:
        offset += MINION_OFFSET
    if i > counts["townsfolk"] + counts["outsider"] + counts["minion"] - 1:
        offset += DEMON_OFFSET

    return offset


def write_script(script_path: str, image_path: str,replacements=REPLACEMENTS):
    script = read_script(script_path)
    replacements = get_replacements(script,replacements)
    script_image = Image.open(image_path)
    counts = calc_character_counts(script)
    for rep in replacements:
        placement = script["characters"].index(rep)
        icon = Image.open(f"./icons/{replacements[rep]}.webp").resize(
            (ICON_SIZE, ICON_SIZE)
        )

        script_image.paste(
            icon,
            (
                INITIAL_X_OFFSET,
                INITIAL_Y_OFFSET + calc_char_offset(placement, counts),
            ),
            icon,
        )

    final_path = image_path.split(".png")[0] + "-REPLACED.png"
    script_image.save(final_path)
    os.system("start" + f""" "dummy" "{final_path}" """)
