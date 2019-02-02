from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .serializers import DiarySerializer
from .models import Diary, DiaryFile
from .forms import DiaryFileForm
import logging
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

logger = logging.getLogger('dairy.users.views')

@api_view(['GET', 'POST'])
@login_required
def diary_list(request):
    """
        get diary list
        /diaries/?page=&page_size=&year=&month&search=&earlier_than=&later_than=&orderBy=
    """
    # logger.debug(repr(DiarySerializer()))
    user_id = request.user.id
    if request.method == 'GET':
        diaries = Diary.objects.all().filter(author=user_id)
        if request.GET.get('year', '') != '':
            diaries = diaries.filter(year=request.GET.get('year'))
        if request.GET.get('month', '') != '':
            diaries = diaries.filter(month=request.GET.get('month'))
        if request.GET.get('search', '') != '':
            diaries = diaries.filter(content__icontains=request.GET.get('search'))
        if request.GET.get('earlier_than', '') != '':
            dt = datetime.strptime(request.GET.get('earlier_than'), settings.REST_FRAMEWORK.get('DATETIME_FORMAT'))
            diaries = diaries.filter(datetime__lt=dt)
        if request.GET.get('later_than', '') != '':
            # logger.debug('later_than={}'.format(request.GET.get('later_than')))
            dt = datetime.strptime(request.GET.get('later_than'), settings.REST_FRAMEWORK.get('DATETIME_FORMAT'))
            # logger.debug('conver to time: {}'.format(dt))
            diaries = diaries.filter(datetime__gt=dt)
        order = request.GET.get('order_by', '-datetime')
        diaries = diaries.order_by(order)
        page = request.GET.get('page')
        if page is None:
            serializer = DiarySerializer(diaries, many=True)
            return JsonResponse({'data': serializer.data}, safe=False)
        else:
            years = Diary.objects.all().values('year').distinct()
            paginator = Paginator(diaries, request.GET.get('page_size', 10))
            serializer = DiarySerializer(paginator.page(page), many=True)
            return JsonResponse({
                'data': serializer.data,
                'num_pages': paginator.num_pages,
                'years': list(years)
                }, safe=False)

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
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        diary.delete()
        return HttpResponse(status=204)

@api_view(['PUT'])
@login_required
def upload_file(request):
    if request.method == 'PUT':
        existing_files = DiaryFile.objects.filter(diary=request.POST.get("diary"))
        for f in existing_files:
            f.file.delete(False)
            f.delete()
        form = DiaryFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'msg': 'ok'})
        else:
            return JsonResponse(form.errors, status=400)
