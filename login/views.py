from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from .language import Language

LOGIN_FILE = "login/main.html"
LANGUAGE   = "en-US" # [PLACEHOLDER]

def home(request):
    return HttpResponseRedirect("/login")

def login(request):
    context = {
        "login_form"    : LoginForm(),
        "register_form" : RegisterForm(),
        "language"      : Language(LANGUAGE)
    }
    return render(request or None, LOGIN_FILE, context)