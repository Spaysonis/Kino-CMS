

from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include

from . import views


urlpatterns = [

    path("", staff_member_required (views.admin), name="statistics"),


    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>/edit/', views.edit_user, name='edit_user'),






    path('content/', staff_member_required(views.content_list), name='content_list'),
    path('content/create/<str:slug>/', views.create_news_or_action, name='content_create'),
    path('content/update/<str:slug>/<int:pk>', views.update_news_or_action, name='content_update'),
    path('content/delete/<int:pk>', views.delete_news_or_action, name='delete_update'),




    path('banners/', views.create_banners, name='banners'),
    path('background-banner/', views.background_banner, name='background_banner'),



    path('movie/', views.movies, name='movies'),
    path('movie/create', views.movie_create_or_update, name='movie_create'),
    path('movie/<int:pk>/update', views.movie_create_or_update, name='movie_update'),
    path('movie/<int:pk>/delete', views.movie_delete, name='movie_delete'),



    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinemas/add', views.cinema_create, name='cinema_create'),
    path('cinemas/<int:pk>/update/', views.cinema_update, name='cinema_update'),
    path('cinema/<int:pk>/delete/', views.cinema_delete, name='cinema_delete'),

    path('cinemas/<int:pk>/hall_create/', views.hall_create, name='hall_create'),
    path('cinemas/<int:cinema_pk>/hall/<int:hall_pk>/update/', views.hall_update, name='hall_update'),
    path('cinemas/<int:cinema_pk>/hall/<int:hall_pk>/delete/', views.hall_delete, name='hall_delete'),








]
