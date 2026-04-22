from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from travels.models import User, Places
from mysite import settings

from loguru import logger

import requests
import json, time

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


def place_events(request):
    if request.method == "GET":
        def event_stream():
            last_snapshot = {}
            while True:
                current_snapshot = {
                    place.id: (place.likes, place.dislikes)
                    for place in Places.objects.all().only("id", "likes", "dislikes")
                }
                for place_id, (likes, dislikes) in current_snapshot.items():
                    previous = last_snapshot.get(place_id)
                    if previous != (likes, dislikes):
                        payload = json.dumps({
                            "place_id": place_id,
                            "likes": likes,
                            "dislikes": dislikes,
                        })
                        yield f"data: {payload}\n\n"

                last_snapshot = current_snapshot

                time.sleep(1)

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response


def add_like(request):
    if request.method == "POST":
        place_id = request.GET.get("data_key") or request.POST.get("data_key")
        if not place_id:
            return JsonResponse({"ok": False, "error": "place id is required"}, status=400)

        place = Places.objects.get(id=place_id)
        place.likes += 1
        place.save()

        return JsonResponse({"ok": True})


def add_dislike(request):
    if request.method == "POST":
        place_id = request.GET.get("data_key") or request.POST.get("data_key")
        if not place_id:
            return JsonResponse({"ok": False, "error": "place id is required"}, status=400)

        place = Places.objects.get(id=place_id)
        place.dislikes += 1
        place.save()

        return JsonResponse({"ok": True})


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
    if request.method != 'POST':
        return render(request, 'travels/index.html')

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()

    payload = {
        "name": name,
        "email": email,
        "message": message,
    }

    try:
        response = requests.post(
            f"{settings.FEEDBACK_SERVICE_URL}/api/v1/feedback",
            json=payload,
            timeout=settings.FEEDBACK_SERVICE_TIMEOUT_SEC,
        )
    except requests.RequestException as exc:
        logger.error(f"Feedback request failed: {exc}")
        return redirect('feedback')

    if response.status_code == 202:
        return render(request, 'travels/feedback_success.html')

    logger.error(f"Feedback service returned error: {response.status_code} - {response.text}")
    return redirect('feedback')


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
                return redirect('login')
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


def logout_process(request):
    request.session.flush()
    return redirect('index')


@csrf_exempt
def add_travel_point(request):
    id_el = request.GET.get('data_key', None)
    if id_el:
        try:
            request.session['travel_points'].append(int(id_el))
            request.session.modified = True
            # logger.info(f"Session: {request.session['travel_points']}")
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


@csrf_exempt
def travel_map(request):
    selected_ids = request.session.get('travel_points', [])
    places = Places.objects.filter(id__in=selected_ids)
    addresses = [{'name': p.name, 'address': p.address} for p in places]
    logger.info(f"Адреса: {addresses}")

    return render(request, 'travels/map.html', {
        'addresses_json': json.dumps(addresses, ensure_ascii=False),
        'api_key': settings.YANDEX_MAPS_API_KEY
    })