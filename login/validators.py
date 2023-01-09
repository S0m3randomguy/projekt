from django.core.exceptions import ValidationError
from projekt.language import Language
from django.db import models
import string
import re

class EmptyValue:
    def __init__(self):
        pass
    
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
        self.cache = {}
    
    def reconstruct(self, key, method):
        self.cache[key] = method
    
    def __call__(self, value):
        print(f"Validating value: {value}")
        for key, method in self.cache.items():
            self.error.params[key] = method(value)

        if not self.condition(value, self):
            raise self.error

class MinLengthValidator(Validator):
    def __init__(self, lang: Language, name, limit):
        super().__init__(
            lang, "min_length_error",
            lambda value, obj: len(value) >= obj.limit,
            name=name, limit=limit
        )

class MaxLengthValidator(Validator):
    def __init__(self, lang: Language, name, limit):
        super().__init__(
            lang, "max_length_error",
            lambda value, obj: len(value) <= obj.limit,
            name=name, limit=limit
        )

class CharsetValidator(Validator):
    def __init__(self, lang: Language, name, chars, *characters):
        super().__init__(
            lang, "charset_error",
            lambda value, obj: not any([x not in "".join(obj.characters) for x in value]),
            name=name, characters=characters,
            chars= ", ".join(chars)
        )

class ExtendedAsciiValidator(CharsetValidator):
    def __init__(self, lang: Language, name):
        chars = [chr(x) for x in range(40, 126)]
        param = lang.sections["other"]["charset_ascii"]
        super().__init__(
            lang, name,
            [param], *chars
        )
    
class AlphanumericValidator(CharsetValidator):
    def __init__(self, lang: Language, name):
        super().__init__(
            lang, name,
            string.ascii_letters,
            string.digits
        )

class RegexValidator(Validator):
    def __init__(self, lang: Language, name, regex, code=None):
        super().__init__(
            lang, code or "regex_error",
            lambda value, obj: len(re.findall(obj.regex, value)) == 1,
            name=name, regex=regex
        )

class EmailValidator(RegexValidator):
    def __init__(self, lang: Language, name):
        expression = r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$"
        super().__init__(
            lang, name,
            expression, "email_error"
        )
        self.reconstruct("email", lambda value: value)

class StrengthValidator(Validator):
    def __init__(self, lang: Language, name):
        characters = (string.digits, string.punctuation, string.ascii_uppercase)
        super().__init__(
            lang, "strength_error",
            lambda value, obj: any([x in obj.characters for x in value]),
            name=name, characters=characters
        )

class DatabaseValidator(Validator):
    def __init__(self, lang: Language, name, model: models.Model, filter, code=None):
        data = model.objects
        super().__init__(
            lang, code or "db_exists_error",
            lambda value, obj: not obj.data.filter(**{
                obj.filter: value
            }),
            name=name, data=data, filter=filter
        )

class RequiredValidator(Validator):
    def __init__(self, lang: Language, name):
        super().__init__(
            lang, "required_error",
            lambda value, obj: not isinstance(value, EmptyValue),
            name=name
        )