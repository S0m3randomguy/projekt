from django.urls import path
from login import views

urlpatterns = [
    path("", views.home, name="Home"),
    path("login/", views.login, name="Login"),
    path("register/", views.register, name="Register")
]