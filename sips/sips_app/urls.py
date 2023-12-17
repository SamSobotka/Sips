from django.urls import path

from . import views
from .views import LoginView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('message/', views.message, name='message'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('post/', views.create_post, name='create_post'),
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('themeselection/', views.themeselection, name='themeselection'),
    path('feed/post/<int:postid>', views.user_post, name='user_post'),
]
