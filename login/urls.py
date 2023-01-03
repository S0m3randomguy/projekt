from django.urls import path
from login import views

urlpatterns = [
    path("login/", views.login, name="Login"),
    path("register/", views.register, name="Register")
]