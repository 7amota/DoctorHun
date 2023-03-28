from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
routers = DefaultRouter()
urlpatterns = [
path('register/', views.RegiserView.as_view()),
path('login/', views.LoginView.as_view()),
path("logout/", views.LogoutView.as_view()),
path("update/", views.UpdateUser.as_view(),),
path("sendemail/", views.ResetRequest.as_view(),),
path("resetpassword/", views.ResetPassword.as_view(),),

]
