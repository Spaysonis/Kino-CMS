


from django.urls import path, include

from . import views
from src.cms import api_views
from .api_views import start_mailing

urlpatterns = [
    path('test', views.test, name='test'),
    path('test/admin/', views.test_admin, name='test_admin'),

    path("", views.admin, name="statistics"),


    path('users/', views.user_list, name='users'),
    path('users/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('users/delete-user/<int:user_id>/', api_views.api_delete_user, name='delete_user'),







    path('content/', views.content_list, name='content_list'),
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


    path('mailing/', views.mailing, name='mailing'),

    path('api/active-mailing/', api_views.active_mailing, name='active_mailing'),
    path('api/upload-mailing/', api_views.upload_mailing_api, name='upload_mailing_api'),
    path('api/delete-mailing/<int:mailing_id>/', api_views.delete_mailing_api, name='delete_mailing_api'),
    path("api/start-mailing/", start_mailing, name="start-mailing"),
    path("api/set_users/", api_views.api_user_modal , name="user_modal"),











]
