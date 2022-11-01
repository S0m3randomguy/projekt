from json import loads
from configparser import ConfigParser

CFG_FILE = "assets/setup.ini"
config = ConfigParser()

config.read(CFG_FILE)

ENCODING = "utf-8"
LANGUAGE = config["language"]["language"]

HEADER  = "assets/languages/{lang}/header.json"
MAIN    = "assets/languages/{lang}/{name}"

class Language:
    def __init__(self, lang: str):
        header: dict    = loads(
            open(HEADER.format(lang=lang), encoding=ENCODING).read()
        )
        file:   dict    = loads(
            open(MAIN.format(lang=lang, name=header["file_name"]), encoding=ENCODING).read()
        )
        for key, value in file.items():
            setattr(self, key, value)