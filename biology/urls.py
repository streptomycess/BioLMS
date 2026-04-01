from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/quiz/', views.lesson_quiz, name='lesson_quiz'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
]