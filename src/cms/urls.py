


from django.urls import path

from . import views

urlpatterns = [
    path("", views.statistics, name="statistics"),
    path('banners', views.banners, name="banners" ),
    path('films', views.films, name="films")
]