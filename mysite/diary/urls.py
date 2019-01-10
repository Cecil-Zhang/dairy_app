from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('<int:pk>/', views.diary_detail),
    path('', views.diary_list),
]