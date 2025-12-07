

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [

    path("", views.admin, name="statistics"),

    path('users/', views.UserListView.as_view(), name='users'),
    path('news/', views.news, name='news'),
    path('movie/', views.movie_edit, name='movie'),
    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinemas/add', views.cinema_create, name='cinema_create'),
    path('cinemas/<int:pk>/edit/', views.cinema_create, name='cinema_edit'),


    path('users/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('test', views.test, name='test')

]


    #path('banners', views.banners, name="banners" ),]
#     path('films', views.films, name="films")
# ]