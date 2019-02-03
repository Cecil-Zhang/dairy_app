from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('info/', views.user_info, name='info'),
    path('changePassword/', views.change_pwd, name='change_pwd')
]