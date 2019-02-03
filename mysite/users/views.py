from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging, json
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers

logger = logging.getLogger('dairy.users.views')

@api_view(['POST'])
@csrf_exempt
def user_login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'id': user.id, 'username': user.username, \
            'first_name': user.first_name, 'last_name': user.last_name}, status=200)
    else:
        return JsonResponse({'error': 'username or password is wrong'}, status=401)

@api_view(['POST'])
@csrf_exempt
def user_logout(request):
    logout(request)
    return HttpResponse(status=204)

@api_view(['POST'])
@csrf_exempt
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@csrf_exempt
def change_pwd(request):
    user = authenticate(username=request.user.username, password=request.data['old'])
    if user is not None:
        user.set_password(request.data['new'])
        user.save()
        return JsonResponse({'msg': 'ok'}, status=200)
    else:
        return JsonResponse({'error': 'password is not correct'}, status=401)

@api_view(['GET', 'PUT'])
@csrf_exempt
def user_info(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data, status=200)
        elif request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'not login yet'}, status=401)
