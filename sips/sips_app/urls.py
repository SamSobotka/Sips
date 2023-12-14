from django.urls import path

from . import views
from .views import LoginView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('message/', views.message, name='message'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('post/', views.post, name='post'),
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('themeselection/', views.themeselection, name='themeselection'),
]
