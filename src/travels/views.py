from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

from travels.models import User, Places

from loguru import logger
import aiohttp


BOT = Bot('5973563978:AAF4bQPXCcfLOg3-vhSD8XZ8-dTk7CFZW9o', session=AiohttpSession())


def index(request):
    places = Places.objects.all()

    categories = {}
    for place in places:
        if place.category not in categories:
            categories[place.category] = []
        categories[place.category].append(place)

    return render(request, "travels/index.html", {'categories': categories})


def selected_places(request):
    return render(request, "travels/selected_places.html")


def feedback(request):
    return render(request, "travels/feedback.html")


def register(request):
    return render(request, 'travels/registration.html')


def login_view(request):
    return render(request, 'travels/login.html')


@csrf_exempt
async def send_feedback_message(request):
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

            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://api.telegram.org/bot{BOT.token}/sendMessage", json=payload) as response:
                    response.raise_for_status()
                    logger.info(await response.json())

                    if response.status == 200 or response.status == 201:
                        return render(request, 'travels/feedback_success.html')
                    
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error: {e.status}")
        except aiohttp.ClientConnectionError:
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


def logout_process(request):
    request.session.flush()
    return redirect('index')