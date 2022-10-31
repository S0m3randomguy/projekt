from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

    username.widget = forms.TextInput(attrs={
        "type"          : "text",
        "placeholder"   : "Username/Email"
    })

    password.widget = forms.TextInput(attrs={
        "type"          : "password",
        "class"         : "password",
        "placeholder"   : "Password",
        "id"            : "password_field_login"
    })

class RegisterForm(forms.Form):
    name        = forms.CharField(max_length=100, required=True)
    username    = forms.CharField(max_length=100, required=True)
    email       = forms.CharField(max_length=100, required=True)
    password    = forms.CharField(max_length=100, required=True)
    confirm     = forms.CharField(max_length=100, required=True)

    name.widget = forms.TextInput(attrs={
        "type"          : "text",
        "placeholder"   : "Full name",
    })

    username.widget = forms.TextInput(attrs={
        "type"          : "text",
        "placeholder"   : "Username"
    })

    email.widget = forms.TextInput(attrs={
        "type"          : "text",
        "placeholder"   : "Email"
    })

    password.widget = forms.TextInput(attrs={
        "type"          : "password",
        "class"         : "password",
        "placeholder"   : "Password",
        "id"            : "password_field_register"
    })

    confirm.widget = forms.TextInput(attrs={
        "type"          : "password",
        "class"         : "password",
        "placeholder"   : "Confirm password",
        "id"            : "confirmation_field"
    })