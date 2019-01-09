from django.urls import path
from django.conf.urls import url, include
# from rest_framework import routers
from . import views

app_name = 'diary'
urlpatterns = [
    path('<int:pk>/', views.diary_detail),
    path('', views.diary_list),
]