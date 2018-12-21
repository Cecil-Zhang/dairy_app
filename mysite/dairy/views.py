from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.utils import timezone
from .models import Dairy


class IndexView(generic.ListView):
    template_name = 'dairy/index.html'
    context_object_name = 'dairy_list'
    
    def get_queryset(self):
        return Dairy.objects.all()

class DetailView(generic.DetailView):
    model = Dairy
    template_name = 'dairy/detail.html'

class DairyForm(ModelForm):
    class Meta:
        model = Dairy
        fields = ['weather', 'content']

def write_dairy(request):
    if request.method == 'POST':
        form = DairyForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            now = timezone.now()
            model_instance.datetime = now
            model_instance.year = now.year
            model_instance.month = now.month
            model_instance.day = now.day
            model_instance.save()
            return redirect('dairy:index')
    else:
        form = DairyForm()
        return render(request, 'dairy/write.html', {'form': form})