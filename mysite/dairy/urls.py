from django.urls import path

from . import views

app_name = 'dairy'
urlpatterns = [
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('write/', views.write_dairy, name='write'),
    path('', views.IndexView.as_view(), name='index'),
]