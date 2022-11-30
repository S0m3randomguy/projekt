from json import loads
from configparser import ConfigParser

ENCODING = "utf-8"

HEADER  = "assets/languages/{lang}/header.json"
MAIN    = "assets/languages/{lang}/{name}"

class Language:
    def __init__(self, lang: str):
        self.lang = lang

        header: dict    = loads(
            open(HEADER.format(lang=lang), encoding=ENCODING).read()
        )
        file:   dict    = loads(
            open(MAIN.format(lang=lang, name=header["file_name"]), encoding=ENCODING).read()
        )
        self.head = header
        self.sections = file