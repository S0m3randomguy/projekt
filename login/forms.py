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
    ExtendedAsciiValidator,
    DatabaseValidator
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
MAX_PASSWORD_LENGTH = config.getint(ACCOUNT_SECTION, "MAX_PASSWORD_LENGTH")

def get_login_form(lang: Language, request=None):
    t = lang.translate
    USERNAME_PLACEHOLDER = t("login.username_placeholder")
    PASSWORD_PLACEHOLDER = t("login.password_placeholder")

    class LoginForm(forms.Form):
        username = forms.CharField(required=True)
        password = forms.CharField(required=True)

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

        def clean(self):
            super(LoginForm, self).clean()
            cleaned: dict = self.cleaned_data
            data = Account.objects

            credentials = data.filter(**cleaned).values()
            if not credentials:
                code = "invalid_credentials"
                raise ValidationError(
                    lang.sections["errors"][code],
                    code=code
                )
            return cleaned
    
    return LoginForm(request.POST if request else None)

def get_register_form(lang: Language, request=None):
    t = lang.translate
    NAME_PLACEHOLDER     = t("register.name_placeholder")
    USERNAME_PLACEHOLDER = t("register.username_placeholder")
    EMAIL_PLACEHOLDER    = t("register.email_placeholder")
    PASSWORD_PLACEHOLDER = t("register.password_placeholder")
    CONFIRM_PLACEHOLDER  = t("register.confirm_placeholder")

    CHARSET_LETTERS      = t("other.charset_letters")
    CHARSET_DIGITS       = t("other.charset_digits")
    CHARSET_UNDERSCORE   = t("other.charset_underscore")
    PARAMS               = [CHARSET_LETTERS, CHARSET_DIGITS, CHARSET_UNDERSCORE]
    CHARSET              = string.ascii_letters + string.digits + "_"

    class RegisterForm(forms.ModelForm):
        name = forms.CharField(required=True, validators=[
            MaxLengthValidator(lang, NAME_PLACEHOLDER, MAX_NAME_LENGTH),
            MinLengthValidator(lang, NAME_PLACEHOLDER, MIN_NAME_LENGTH)
        ])
        username = forms.CharField(required=True, validators=[
            MaxLengthValidator(lang, USERNAME_PLACEHOLDER, MAX_USERNAME_LENGTH),
            MinLengthValidator(lang, USERNAME_PLACEHOLDER, MIN_USERNAME_LENGTH),
            CharsetValidator(lang, USERNAME_PLACEHOLDER, PARAMS, CHARSET),
            DatabaseValidator(lang, USERNAME_PLACEHOLDER, Account, "username")
        ])
        email = forms.CharField(required=True, validators=[
            EmailValidator(lang, EMAIL_PLACEHOLDER),
            DatabaseValidator(lang, EMAIL_PLACEHOLDER, Account, "email")
        ])
        password = forms.CharField(required=True, validators=[
            MaxLengthValidator(lang, PASSWORD_PLACEHOLDER, MAX_PASSWORD_LENGTH),
            MinLengthValidator(lang, PASSWORD_PLACEHOLDER, MIN_PASSWORD_LENGTH),
            ExtendedAsciiValidator(lang, PASSWORD_PLACEHOLDER)
        ])
        confirm = forms.CharField(required=True, validators=[
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

            if cleaned.get("password", None) != cleaned.get("confirm", None):
                code = "mismatch_error"
                raise ValidationError(
                    lang.sections["errors"][code],
                    code=code
                )
            return cleaned

    return RegisterForm(request.POST if request else None)