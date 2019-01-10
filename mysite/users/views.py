from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging, json
from rest_framework.decorators import api_view
from .serializers import UserSerializer

logger = logging.getLogger('dairy.users.views')

@csrf_exempt
@api_view(['POST'])
def user_login(request):
    body = json.loads(request.body)
    username = body['username']
    password = body['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        for it in request.session.items():
            logger.debug(it)
        return JsonResponse({'id': user.id, 'username': user.username, \
            'first_name': user.first_name, 'last_name': user.last_name}, status=200)
    else:
        return JsonResponse({'error': 'username or password is wrong'}, status=401)

@csrf_exempt
@api_view(['POST'])
def user_logout(request):
    logout(request)
    return HttpResponse(status=204)

@csrf_exempt
@api_view(['POST'])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)