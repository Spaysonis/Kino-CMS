from django.urls import path

from . import views
from .views_api import get_schedules_ajax, confirm_booking
from django.views.i18n import set_language

urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),
    path("", views.main, name="main"),
    path("movie/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("movie/<int:pk>/schedules/", get_schedules_ajax, name="movie-schedules-ajax"),
    path('booking/<int:pk>/', views.booking, name='booking'),
    path("sessions/<int:pk>/confirm/", confirm_booking, name="confirm_booking"),




    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='logout'),


    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('cinema/', views.cinema_list1, name='cinema_list1'),


    path('poster/', views.poster_coming, name='poster'),
    path('schedule/', views.schedule, name='schedule')
]