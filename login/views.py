from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from projekt.language import *
import os

LOGIN_FILE      = "login/main.html"
REGISTER_FILE   = "register/main.html"
GET_FORM = {
    "login"     : get_login_form,
    "register"  : get_register_form
}

def form_method(form_name, template):
    def method(request):
        lang = request.GET.get("lang", None)
        language = Language(verify_language(lang) or "en-US")

        form_method = GET_FORM.get(form_name, None)
        if form_method is None:
            return HttpResponseRedirect("/")
        form = form_method(language, request)
        
        if request.method == "POST":
            if form.is_valid():
                return HttpResponseRedirect("/test")
            else:
                print(form.errors.as_json())

        context = {
            f"{form_name}_form"    : form,
            "language"             : language
        }
        return render(request or None, template, context)
    return method

def home(request):
    return HttpResponseRedirect("/login")

def login(request):
    method = form_method("login", LOGIN_FILE)
    return method(request)

def register(request):
    method = form_method("register", REGISTER_FILE)
    return method(request)

def verify_language(lang: str):
    languages = [name for name in os.listdir("assets/languages")]
    return lang if lang in languages else None