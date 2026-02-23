# chat/urls.py
from django.contrib.auth import admin
from django.urls import path, include

from src.chat import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]