from django import forms
from projekt.language import *
from .models import Account
from configparser import ConfigParser
from django.core.exceptions import ValidationError
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
MIN_NAME_LENGTH     = config.getint(ACCOUNT_SECTION, "MIN_NAME_LENGTH")
MAX_NAME_LENGTH     = config.getint(ACCOUNT_SECTION, "MAX_NAME_LENGTH")

MIN_USERNAME_LENGTH = config.getint(ACCOUNT_SECTION, "MIN_USERNAME_LENGTH")
MAX_USERNAME_LENGTH = config.getint(ACCOUNT_SECTION, "MAX_USERNAME_LENGTH")

MIN_PASSWORD_LENGTH = config.getint(ACCOUNT_SECTION, "MIN_PASSWORD_LENGTH")
MAX_PASSWORD_LENGTH = config.getint(ACCOUNT_SECTION, "MIN_PASSWORD_LENGTH")

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
    SECTION_REGISTER     = lang.sections["register"]

    NAME_PLACEHOLDER     = SECTION_REGISTER["name_placeholder"]
    USERNAME_PLACEHOLDER = SECTION_REGISTER["username_placeholder"]
    EMAIL_PLACEHOLDER    = SECTION_REGISTER["email_placeholder"]
    PASSWORD_PLACEHOLDER = SECTION_REGISTER["password_placeholder"]
    CONFIRM_PLACEHOLDER  = SECTION_REGISTER["confirm_placeholder"]

    SECTION_OTHER        = lang.sections["other"]

    CHARSET_LETTERS      = SECTION_OTHER["charset_letters"]
    CHARSET_DIGITS       = SECTION_OTHER["charset_digits"]
    CHARSET_UNDERSCORE   = SECTION_OTHER["charset_underscore"]
    PARAMS               = [CHARSET_LETTERS, CHARSET_DIGITS, CHARSET_UNDERSCORE]
    CHARSET              = string.ascii_letters + string.digits + "_"

    class RegisterForm(forms.ModelForm):
        name = forms.CharField(max_length=MAX_NAME_LENGTH, required=True, validators=[
            MaxLengthValidator(lang, NAME_PLACEHOLDER, MAX_NAME_LENGTH),
            MinLengthValidator(lang, NAME_PLACEHOLDER, MIN_NAME_LENGTH),
            CharsetValidator(lang, NAME_PLACEHOLDER, PARAMS, CHARSET)
        ])
        username = forms.CharField(max_length=MAX_USERNAME_LENGTH, required=True, validators=[
            MaxLengthValidator(lang, USERNAME_PLACEHOLDER, MAX_USERNAME_LENGTH),
            MinLengthValidator(lang, USERNAME_PLACEHOLDER, MIN_USERNAME_LENGTH),
            CharsetValidator(lang, USERNAME_PLACEHOLDER, PARAMS, CHARSET)
        ])
        email = forms.CharField(required=True, validators=[
            EmailValidator(lang, EMAIL_PLACEHOLDER)
        ])
        password = forms.CharField(max_length=MAX_PASSWORD_LENGTH, required=True, validators=[
            MaxLengthValidator(lang, PASSWORD_PLACEHOLDER, MAX_PASSWORD_LENGTH),
            MinLengthValidator(lang, PASSWORD_PLACEHOLDER, MIN_PASSWORD_LENGTH),
            ExtendedAsciiValidator(lang, PASSWORD_PLACEHOLDER)
        ])
        confirm = forms.CharField(max_length=MAX_PASSWORD_LENGTH, required=True, validators=[
            MaxLengthValidator(lang, CONFIRM_PLACEHOLDER, MAX_PASSWORD_LENGTH),
            MinLengthValidator(lang, CONFIRM_PLACEHOLDER, MIN_PASSWORD_LENGTH),
            ExtendedAsciiValidator(lang, CONFIRM_PLACEHOLDER)
        ])
        
        name.widget = forms.TextInput(attrs={
            "type"          : "text",
            "placeholder"   : NAME_PLACEHOLDER,
        })
        username.widget =  forms.TextInput(attrs={
            "type"          : "text",
            "placeholder"   : USERNAME_PLACEHOLDER,
        })
        email.widget = forms.TextInput(attrs={
            "type"          : "text",
            "placeholder"   : EMAIL_PLACEHOLDER,
        })
        password.widget = forms.TextInput(attrs={
            "type"          : "password",
            "class"         : "password",
            "placeholder"   : PASSWORD_PLACEHOLDER,
            "id"            : "password_field_register"
        })
        confirm.widget = forms.TextInput(attrs={
            "type"          : "password",
            "class"         : "password",
            "placeholder"   : CONFIRM_PLACEHOLDER,
            "id"            : "confirmation_field"
        })
        
        class Meta:
            model = Account
            fields = ["name", "username", "email", "password", "confirm"]

        def clean(self):
            super(RegisterForm, self).clean()
            cleaned = self.cleaned_data
            return cleaned

    return RegisterForm(request.POST if request else None)