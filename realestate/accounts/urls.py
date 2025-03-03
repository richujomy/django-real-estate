from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),  # Changed to user_login
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('logout/', views.logout_view, name='logout'),
   
]