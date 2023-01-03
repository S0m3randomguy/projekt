from json import loads
from functools import reduce
import string

LETTERS = string.ascii_letters
DIGITS = string.digits

ENCODING = "utf-8"

HEADER  = "assets/languages/{lang}/header.json"
MAIN    = "assets/languages/{lang}/{name}"

class Result:
    def __init__(self):
        self.error = None
        self.value = None
    
    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self

class Language:
    def __init__(self, lang: str):
        self.lang = lang

        header: dict = loads(
            open(HEADER.format(lang=lang), encoding=ENCODING).read()
        )
        file: dict = loads(
            open(MAIN.format(lang=lang, name=header["file_name"]), encoding=ENCODING).read()
        )
        self.head = header
        self.sections = file

    def get(self, keys):
        return reduce(lambda c, k: c.get(k, {}), keys, self.sections)

    def translate(self, string: str):
        if "." in string:
            path = string.split(".")
        else: path = [string]

        if any([not x for x in path]): raise Exception(
            f"Invalid path: '{string}'"
        )
        
        result = self.get(path)
        if not result: raise Exception(
            f"Cannot find item '{path[-1]}'"
        )
        return result
