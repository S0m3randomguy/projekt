from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *

LOGIN_FILE = "login/main.html"

def home(request):
    return HttpResponseRedirect("/login")

def login(request):
    context = {}
    context["login_form"] = LoginForm()
    context["register_form"] = RegisterForm()
    return render(request or None, LOGIN_FILE, context)