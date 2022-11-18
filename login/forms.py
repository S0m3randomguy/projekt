from django import forms
from projekt.language import *

language = Language(LANGUAGE)

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
    
    return LoginForm(data=request)

def get_register_form(lang: Language, request=None):
    SECTION_REGISTER            = lang.sections["register"]

    FULL_NAME_PLACEHOLDER       = SECTION_REGISTER["full_name_placeholder"]
    USERNAME_PLACEHOLDER        = SECTION_REGISTER["username_placeholder"]
    EMAIL_PLACEHOLDER           = SECTION_REGISTER["email_placeholder"]
    PASSWORD_PLACEHOLDER        = SECTION_REGISTER["password_placeholder"]
    CONFIRMATION_PLACEHOLDER    = SECTION_REGISTER["confirmation_placeholder"]

    class RegisterForm(forms.Form):
        name        = forms.CharField(max_length=100, required=True)
        username    = forms.CharField(max_length=100, required=True)
        email       = forms.CharField(max_length=100, required=True)
        password    = forms.CharField(max_length=100, required=True)
        confirm     = forms.CharField(max_length=100, required=True)

        name.widget = forms.TextInput(attrs={
            "type"          : "text",
            "placeholder"   : FULL_NAME_PLACEHOLDER,
        })

        username.widget = forms.TextInput(attrs={
            "type"          : "text",
            "placeholder"   : USERNAME_PLACEHOLDER
        })

        email.widget = forms.TextInput(attrs={
            "type"          : "text",
            "placeholder"   : EMAIL_PLACEHOLDER
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
            "placeholder"   : CONFIRMATION_PLACEHOLDER,
            "id"            : "confirmation_field"
        })

    return RegisterForm(data=request)