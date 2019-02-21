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
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models.functions import Left
from django.db.models import Count
from .render import Render
from django.views.generic import View
from django.utils.safestring import mark_safe

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
        # max_content = request.GET.get('content_truncate', 50)
        # diaries = diaries.annotate(truncate=Left('content', max_content), pic_count=Count('pictures'))
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
        form = DiaryFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'msg': 'ok'})
        else:
            return JsonResponse(form.errors, status=400)

@api_view(['DELETE'])
@login_required
def delete_file(request, diary_id, file_id):
    if request.method == 'DELETE':
        file = DiaryFile.objects.filter(diary=diary_id, id=file_id)
        for f in file:
            f.file.delete(False)
            f.delete()
        return HttpResponse(status=204)

def get_month_diaries(year, mont, line_length=40):
    if year is None or month is None:
        lastmonth = datetime.today().replace(day=1) - timedelta(days=1)
        year = lastmonth.year
        month = lastmonth.month
    diaries = Diary.objects.all().filter(month=month, year=year).order_by('day')
    for diary in diaries:
        newContent = ''
        line_count = 2
        low = 0
        for i in range(0, len(diary.content)):
            if diary.content[i] == '\n':
                line_count = 1
            elif line_count == line_length:
                newContent = newContent + diary.content[low:i] + '\n'
                line_count = 0
                low = i
            line_count = line_count + 1
        diary.content = newContent + diary.content[low:]
    return diaries

class MonthView(View):
    def get(self, request):
        diaries = get_month_diaries(request.GET.get('year'), request.GET.get('month'))
        params = {
            'diaries': diaries
        }
        format = request.GET.get('format', 'pdf')
        if format == 'pdf':
            return Render.render('diary/monthView.html', params)
        else:
            return render(request, 'diary/monthView.html', params)