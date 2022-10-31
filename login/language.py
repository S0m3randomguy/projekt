from json import loads

HEADER  = "assets/languages/{lang}/header.json"
MAIN    = "assets/languages/{lang}/{name}"

class Language:
    def __init__(self, lang: str):
        header: dict    = loads(
            open(HEADER.format(lang=lang)).read()
        )
        file:   dict    = loads(
            open(MAIN.format(lang=lang, name=header["file_name"])).read()
        )

        for key, value in file.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        result = self.__dict__
        return result