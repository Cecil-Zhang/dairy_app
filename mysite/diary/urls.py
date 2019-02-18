from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('upload/', views.upload_file),
    path('<int:diary_id>/files/<int:file_id>/', views.delete_file),
    path('<int:pk>/', views.diary_detail),
    path('', views.diary_list),
]