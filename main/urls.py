from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router =    DefaultRouter()
router.register('',views.Appointemtns)
urlpatterns = [
    path('main/', views.MainPage.as_view()),
    path('live/', views.LiveDoctor.as_view()),
    path('view/', views.DoctroView.as_view()),
    path('rate/', views.Rate.as_view()),
    path('like/', views.Like.as_view()),
    path('doctors/', views.DoctorsList.as_view()),
    path('appointment/', views.Appointemtns.as_view()),
    path('appointment/<int:id>/', views.AppointemntsRUD.as_view()),
]
