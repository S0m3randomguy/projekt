from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from projekt.language import *
import os

LOGIN_FILE      = "login/main.html"
REGISTER_FILE   = "register/main.html"

def process_login(request, form: forms.Form):
    response = HttpResponseRedirect("/")
    response.set_cookie("username", form.cleaned_data["username"])
    return response

def process_register(request, form: forms.ModelForm):
    form.save(commit=True)
    return HttpResponseRedirect("/")

def form_method(request, method, process, file):
    lang = request.GET.get("lang", None)
    language = Language(verify_language(lang) or "en-US")
    form, assets = method(language, request)

    context = {
        "form"     : form,
        "language" : language,
        "assets"   : assets
    }

    response = render(request or None, file, context)

    if request.method == "POST":
        if form.is_valid():
            response = process(request, form)
        else: print(form.errors.as_json())

    return response

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