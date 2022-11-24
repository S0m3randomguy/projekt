from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from projekt.language import *
import os

LOGIN_FILE      = "login/main.html"
REGISTER_FILE   = "register/main.html"

def form_method(func, template):
    def method(request):
        lang = request.GET.get("lang", None)
        language = Language(verify_language(lang) or "en-US")

        if request.method == "POST":
            form = func(language, request)
            if form.is_valid():
                # todo
                return HttpResponseRedirect("/test")

        context = {
            "login_form"    : get_login_form(language),
            "language"      : language
        }
        return render(request or None, template, context)
    return method

def home(request):
    return HttpResponseRedirect("/login")

def login(request):
    method = form_method(get_login_form, LOGIN_FILE)
    return method(request)

def register(request):
    method = form_method(get_register_form, REGISTER_FILE)
    return method(request)

def verify_language(lang: str):
    languages = [name for name in os.listdir("assets/languages")]
    return lang if lang in languages else None