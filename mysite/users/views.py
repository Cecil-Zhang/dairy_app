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

@login_required
@api_view(['GET'])
@csrf_exempt
def user_info(request):
    user = User.objects.get(pk=request.user.id)
    return JsonResponse({'id': user.id, 'username': user.username, \
        'first_name': user.first_name, 'last_name': user.last_name}, status=200)
