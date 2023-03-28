from django.urls import path
from . import views
urlpatterns = [
    path('main/', views.MainPage.as_view()),
    path('live/', views.LiveDoctor.as_view()),
    path('view/', views.DoctroView.as_view()),
    path('rate/', views.Rate.as_view()),
    path('like/', views.Like.as_view()),
    path('filter/', views.DoctorsList.as_view()),
]
