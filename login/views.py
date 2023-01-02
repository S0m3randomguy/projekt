from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from projekt.language import *
import os

LOGIN_FILE      = "login/main.html"
REGISTER_FILE   = "register/main.html"

def process_login(form: forms.Form):
    # login
    return HttpResponseRedirect("/")

def process_register(form: forms.ModelForm):
    form.save(commit=True)
    return HttpResponseRedirect("/")

def form_method(request, method, process, file):
    lang = request.GET.get("lang", None)
    language = Language(verify_language(lang) or "en-US")
    form = method(language, request)
    
    if request.method == "POST":
        if form.is_valid():
            return process(form)
        else: print(form.errors.as_json())

    context = {
        "form"     : form,
        "language" : language
    }
    return render(request or None, file, context)

def home(request):
    return HttpResponseRedirect("/login")

def login(request):
    result = form_method(
        request,
        get_login_form,
        process_login,
        LOGIN_FILE
    )
    return result

def register(request):
    result = form_method(
        request,
        get_register_form,
        process_register,
        REGISTER_FILE
    )
    return result

def verify_language(lang: str):
    languages = [name for name in os.listdir("assets/languages")]
    return lang if lang in languages else None