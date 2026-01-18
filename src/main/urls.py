from django.urls import path

from . import views


urlpatterns = [
    path("", views.main, name="main"),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),

    path('logout/', views.logout_view, name='logout'),

    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('cinema/', views.cinema_list1, name='cinema_list1'),
]