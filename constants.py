import json
import get_characters
CHARACTERS: list[get_characters.Character]= []
try:
    CHARACTERS = json.load(open("./roles.json"))
except:
    CHARACTERS = get_characters.get_chars()
