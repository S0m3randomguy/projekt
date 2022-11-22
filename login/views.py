from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from projekt.language import *
import os

LOGIN_FILE = "login/main.html"
GET_FORM = {
    "login"     : get_login_form,
    "register"  : get_register_form
}

def home(request):
    return HttpResponseRedirect("/login")

def login(request):
    lang = request.GET.get("lang", None)
    language = Language(verify_language(lang) or "en-US")

    if request.method == "POST":
        form_type = request.POST.get("form", None)
        form = GET_FORM.get(form_type, get_login_form)(language, request.POST)

        if form.is_valid():
            # todo
            return HttpResponseRedirect("/test")

    context = {
        "login_form"    : get_login_form(language),
        "register_form" : get_register_form(language),
        "language"      : language
    }
    return render(request or None, LOGIN_FILE, context)


def verify_language(lang: str):
    languages = [name for name in os.listdir("assets/languages")]
    return lang if lang in languages else None