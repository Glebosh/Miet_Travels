from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("selected/", views.selected_places, name="selected_places"),
    path("feedback/", views.feedback, name="feedback"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("send-feedback/", views.send_feedback_message, name="send-feedback"),
    path('reg-process', views.reg_process, name="reg-process"),
    path('log-process', views.log_process, name="log-process"),
    path('logout-process', views.logout_process, name="logout-process"),
    path('add-travel-point', views.add_travel_point, name="add-travel-point"),
    path('remove-travel-point', views.remove_travel_point, name="remove-travel-point"),
    path('travel-map', views.travel_map, name="travel-map"),
    path("places/events/", views.place_events, name="place-events"),
    path("add-like/", views.add_like, name="add-like"),
    path("add-dislike/", views.add_dislike, name="add-dislike"),
]