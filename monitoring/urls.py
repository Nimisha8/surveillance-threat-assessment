from django.urls import path
from . import views

urlpatterns = [
    path('video_feed/', views.video_feed, name='video_feed'),
    path('latest_threat/', views.latest_threat, name='latest_threat'),
]