from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .serializers import DiarySerializer
from .models import Diary
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('dairy.users.views')

@api_view(['GET', 'POST'])
@login_required
@csrf_exempt
def diary_list(request):
    # logger.debug(repr(DiarySerializer()))
    user_id = request.user.id
    if request.method == 'GET':
        diaries = Diary.objects.all().filter(author=user_id)
        if len(diaries) > 0:
            serializer = DiarySerializer(diaries, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'code': 404, 'msg': "No diary yet"})        

    elif request.method == 'POST':
        data = request.data
        data['author'] = request.user.id
        serializer = DiarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@login_required
@csrf_exempt
def diary_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        diary = Diary.objects.get(pk=pk)
    except Diary.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DiarySerializer(diary)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = DiarySerializer(diary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        diary.delete()
        return HttpResponse(status=204)

@api_view(['POST'])
@login_required
@csrf_exempt
def write_dairy(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            now = timezone.now()
            model_instance.datetime = now
            model_instance.year = now.year
            model_instance.month = now.month
            model_instance.day = now.day
            model_instance.save()
            return redirect('diary:index')
