from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
routers = DefaultRouter()
urlpatterns = [
path('users/register', views.RegiserView.as_view()),
path('users/login', views.LoginView.as_view()),


]
