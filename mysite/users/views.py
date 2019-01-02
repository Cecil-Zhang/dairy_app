from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging, json

@csrf_exempt
def user_login(request):
    body = json.loads(request.body)
    username = body['username']
    password = body['password']
    # logging.debug(username)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'error': 'user not found'})