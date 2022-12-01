from django.core.exceptions import ValidationError
from projekt.language import Language
import string
import re

def get_error_message(lang: Language, code):
    return lang.sections["errors"][code]

class Validator:
    def __init__(self, lang: Language, code, condition, **kwargs):
        message = get_error_message(lang, code)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.condition = condition

        self.error = ValidationError(
            message, code=code,
            params=kwargs
        )
    
    def __call__(self, value):
        if not self.condition(value, self):
            raise self.error

class MinLengthValidator(Validator):
    def __init__(self, lang: Language, name, limit):
        super().__init__(
            lang, "min_length_error",
            lambda value, obj: value >= obj.limit,
            name=name, limit=limit
        )

class MaxLengthValidator(Validator):
    def __init__(self, lang: Language, name, limit):
        super().__init__(
            lang, "max_length_error",
            lambda value, obj: value < obj.limit,
            name=name, limit=limit
        )

class CharsetValidator(Validator):
    def __init__(self, lang: Language, name, *characters):
        super().__init__(
            lang, "charset_error",
            lambda value, obj: value not in "".join(obj.chars),
            name=name, chars=characters
        )
    
class AlphanumericValidator(CharsetValidator):
    def __init__(self, lang: Language, name):
        super().__init__(
            lang, name,
            string.ascii_letters + string.digits
        )

class RegexValidator(Validator):
    def __init__(self, lang: Language, name, regex, code=None):
        super().__init__(
            lang, code or "regex_error",
            lambda value, obj: len(re.findall(obj.regex, value)) == 1,
            name=name, regex=regex
        )