from django import forms
from projekt.language import *
from .models import Account
from configparser import ConfigParser
from .validators import (
    MinLengthValidator,
    MaxLengthValidator,
    CharsetValidator,
    EmailValidator,
    ExtendedAsciiValidator
)
import string

CONFIG_FILE = "assets/setup.ini"
config = ConfigParser()
config.read(CONFIG_FILE)

ACCOUNT_SECTION     = "account"
MIN_NAME_LENGTH     = config.get(ACCOUNT_SECTION, "MIN_NAME_LENGTH")
MAX_NAME_LENGTH     = config.get(ACCOUNT_SECTION, "MAX_NAME_LENGTH")

MIN_USERNAME_LENGTH = config.get(ACCOUNT_SECTION, "MIN_USERNAME_LENGTH")
MAX_USERNAME_LENGTH = config.get(ACCOUNT_SECTION, "MAX_USERNAME_LENGTH")

MIN_PASSWORD_LENGTH = config.get(ACCOUNT_SECTION, "MIN_PASSWORD_LENGTH")
MAX_PASSWORD_LENGTH = config.get(ACCOUNT_SECTION, "MIN_PASSWORD_LENGTH")

def get_login_form(lang: Language, request=None):
    SECTION_LOGIN        = lang.sections["login"]

    USERNAME_PLACEHOLDER = SECTION_LOGIN["username_placeholder"]
    PASSWORD_PLACEHOLDER = SECTION_LOGIN["password_placeholder"]

    class LoginForm(forms.Form):
        username = forms.CharField(max_length=100, required=True)
        password = forms.CharField(max_length=100, required=True)

        username.widget = forms.TextInput(attrs={
            "type"          : "text",
            "placeholder"   : USERNAME_PLACEHOLDER
        })

        password.widget = forms.TextInput(attrs={
            "type"          : "password",
            "class"         : "password",
            "placeholder"   : PASSWORD_PLACEHOLDER,
            "id"            : "password_field_login"
        })
    
    return LoginForm(request.POST if request else None)

def get_register_form(lang: Language, request=None):
    SECTION_REGISTER            = lang.sections["register"]

    FULL_NAME_PLACEHOLDER       = SECTION_REGISTER["full_name_placeholder"]
    USERNAME_PLACEHOLDER        = SECTION_REGISTER["username_placeholder"]
    EMAIL_PLACEHOLDER           = SECTION_REGISTER["email_placeholder"]
    PASSWORD_PLACEHOLDER        = SECTION_REGISTER["password_placeholder"]
    CONFIRMATION_PLACEHOLDER    = SECTION_REGISTER["confirmation_placeholder"]
    

    class RegisterForm(forms.ModelForm):
        class Meta:
            model = Account
            fields = ["name", "username", "email", "password", "confirm"]
            widgets = {
                "name" : forms.TextInput(attrs={
                    "type"          : "text",
                    "placeholder"   : FULL_NAME_PLACEHOLDER,
                }),
                "username": forms.TextInput(attrs={
                    "type"          : "text",
                    "placeholder"   : USERNAME_PLACEHOLDER,
                }),
                "email": forms.TextInput(attrs={
                    "type"          : "text",
                    "placeholder"   : EMAIL_PLACEHOLDER,
                }),
                "password": forms.TextInput(attrs={
                    "type"          : "password",
                    "class"         : "password",
                    "placeholder"   : PASSWORD_PLACEHOLDER,
                    "id"            : "password_field_register"
                }),
                "confirm": forms.TextInput(attrs={
                    "type"          : "password",
                    "class"         : "password",
                    "placeholder"   : CONFIRMATION_PLACEHOLDER,
                    "id"            : "confirmation_field"
                })
            }
            validators = {
                "name": [
                    MinLengthValidator(
                        lang, FULL_NAME_PLACEHOLDER,
                        MIN_NAME_LENGTH
                    ),
                    MaxLengthValidator(
                        lang, FULL_NAME_PLACEHOLDER,
                        MAX_NAME_LENGTH
                    ),
                ],
                "username": [
                    MinLengthValidator(
                        lang, USERNAME_PLACEHOLDER,
                        MIN_USERNAME_LENGTH
                    ),
                    MaxLengthValidator(
                        lang, USERNAME_PLACEHOLDER,
                        MAX_USERNAME_LENGTH
                    ),
                    CharsetValidator(
                        lang, USERNAME_PLACEHOLDER,
                        string.ascii_letters + string.digits + "_"
                    )
                ],
                "email": [
                    EmailValidator(
                        lang, EMAIL_PLACEHOLDER
                    )
                ],
                "password": [
                    MinLengthValidator(
                        lang, PASSWORD_PLACEHOLDER,
                        MIN_PASSWORD_LENGTH
                    ),
                    MaxLengthValidator(
                        lang, PASSWORD_PLACEHOLDER,
                        MAX_PASSWORD_LENGTH
                    ),
                    ExtendedAsciiValidator(
                        lang, PASSWORD_PLACEHOLDER
                    )
                ]
            }

        def clean(self):
            cleaned = super().clean()
            name        = cleaned.get("name")
            username    = cleaned.get("username")
            email       = cleaned.get("email")
            password    = cleaned.get("password")
            confirm     = cleaned.get("confirm")

    return RegisterForm(request.POST if request else None)