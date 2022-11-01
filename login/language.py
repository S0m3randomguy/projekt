from json import loads

ENCODING = "utf-8"
LANGUAGE = "hr"

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