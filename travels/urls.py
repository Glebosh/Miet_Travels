from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("selected/", views.selected_places, name="selected_places"),
    path("feedback/", views.feedback, name="feedback"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
]