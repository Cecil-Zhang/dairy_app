from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.utils import timezone
from .models import Diary


class IndexView(generic.ListView):
    template_name = 'diary/index.html'
    context_object_name = 'diary_list'
    
    def get_queryset(self):
        return Diary.objects.all()

class DetailView(generic.DetailView):
    model = Diary
    template_name = 'diary/detail.html'

class DiaryForm(ModelForm):
    class Meta:
        model = Diary
        fields = ['weather', 'content']

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
    else:
        form = DiaryForm()
        return render(request, 'diary/write.html', {'form': form})