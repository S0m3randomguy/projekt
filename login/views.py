from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from projekt.language import *
import os

LOGIN_FILE = "login/main.html"

def home(request):
    return HttpResponseRedirect("/login")

def login(request):
    if request.method == "GET":
        language = request.GET.get("lang", None)
        context = {
            "login_form"    : LoginForm(),
            "register_form" : RegisterForm(),
            "language"      : Language(verify_language(language) or "en-US")
        }
        return render(request or None, LOGIN_FILE, context)

def verify_language(lang: str):
    languages = [name for name in os.listdir("assets/languages")]
    return lang if lang in languages else None