from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

from travels.models import User, Places

from loguru import logger
import requests


BOT = Bot('5973563978:AAF4bQPXCcfLOg3-vhSD8XZ8-dTk7CFZW9o', session=AiohttpSession())


def index(request):
    places = Places.objects.all()

    categories = {}
    for place in places:
        if place.category not in categories:
            categories[place.category] = []
        categories[place.category].append(place)

    try:
        return render(request, "travels/index.html", {
            'categories': categories,
            'travel_points_ids': request.session['travel_points']
        })
    except KeyError:
        return render(request, "travels/index.html", {
            'categories': categories,
            'travel_points_ids': []
        })


def selected_places(request):
    try:
        places = Places.objects.all().order_by('id')

        places_to_visit = []
        count = 0
        logger.info(places)

        for place_id in request.session['travel_points']:
            count += 1
            places_to_visit.append(places[int(place_id) - 1])

        return render(request, "travels/selected_places.html", {
            'places_to_visit': places_to_visit,
            'places_number': count
        })
    
    except KeyError:
        return render(request, "travels/selected_places.html", {
            'places_to_visit': [],
            'places_number': 0
        })


def feedback(request):
    return render(request, "travels/feedback.html")


def register(request):
    return render(request, 'travels/registration.html')


def login_view(request):
    return render(request, 'travels/login.html')


@csrf_exempt
def send_feedback_message(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            full_message = f"Сообщение от {name}: \n\n{message}\n\n Почта пользователя: {email}"

            payload = {
                'chat_id': "268399534",
                'text': full_message,
            }

            response = requests.post(
                f"https://api.telegram.org/bot{BOT.token}/sendMessage",
                json=payload
            )

            if response.status_code in (200, 201):
                return render(request, 'travels/feedback_success.html')

        except requests.ConnectionError:
            print("No connection")
        except Exception as e:
            logger.error(f"Error: {e}")

    return render(request, 'travels/index.html')


@csrf_exempt
def reg_process(request):
    if request.method == 'POST':
        try:
            if not User.objects.filter(email=request.POST.get('email')).exists():
                user = User.objects.create(
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    age=request.POST.get('age'),
                    email=request.POST.get('email'),
                    password=make_password(request.POST.get('password')),
                )
                logger.info(f"Has been created User: {user}")
                return redirect('registration')
            else:
                logger.error("User with same email exists")
                messages.error(request, "Пользователь с данной почтой уже существует!")
                return redirect('register')

        except Exception as e:
            logger.error(f"Error: {e}")

    return render(request, 'travels/index.html')


@csrf_exempt
def log_process(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_name'] = user.first_name
                request.session['travel_points'] = []
                logger.info("Successful log proccess")
                return redirect('index')
            else:
                messages.error(request, "Неверный пароль!")
                return redirect('login')
            
        except User.DoesNotExist:
            logger.error("User not found")
            messages.error(request, "Пользователь не найден!")
            return redirect('login')
        
        except Exception as e:
            logger.info(f"Error: {e}")
    
    return render(request, 'travels/index.html')


@csrf_exempt
def add_travel_point(request):
    id_el = request.GET.get('data_key', None)
    if id_el:
        try:
            request.session['travel_points'].append(int(id_el))
            request.session.modified = True
            logger.info(f"Session: {request.session['travel_points']}")
            return redirect(f'/travels/#place-{id_el}')
        except Exception as e:
            logger.error(f"Error: {e}")
    return redirect('index')


@csrf_exempt
def remove_travel_point(request):
    id_el = request.GET.get('data_key', None)
    if id_el:
        try:
            request.session['travel_points'].remove(int(id_el))
            request.session.modified = True
            return redirect(f'/travels/#place-{id_el}')
            # logger.info(f"Session: {request.session['travel_points']}")
        except Exception as e:
            logger.error(f"Error: {e}")
    return redirect('index')


def logout_process(request):
    request.session.flush()
    return redirect('index')