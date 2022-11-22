from django.core.exceptions import ValidationError
from projekt.language import Language

class MinLengthValidator:
    def __init__(self, lang: Language, value, name, limit):
        SECTIONS_ERROR = lang.sections["errors"]
        ERROR_MESSAGE  = SECTIONS_ERROR["min_length_error"]

        self.name  = name
        self.limit = limit
        self.error = ValidationError(
            ERROR_MESSAGE, code="min_length_error",
            params={
                "name": self.name, "limit": self.limit
            }
        )
    
    def __call__(self, value):
        if not value > self.limit:
            raise self.error