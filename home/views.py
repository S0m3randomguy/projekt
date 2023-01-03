from django.shortcuts import render
from django.http import HttpResponse

HOME_FILE = "home/main.html"

def home(request):
    response = render(request, HOME_FILE)
    return response