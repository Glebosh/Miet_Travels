from django.shortcuts import render


def index(request):
    return render(request, "travels/index.html")


def selected_places(request):
    return render(request, "travels/selected_places.html")


def feedback(request):
    return render(request, "travels/feedback.html")


def register(request):
    return render(request, 'travels/registration.html')


def login_view(request):
    return render(request, 'travels/login.html')