

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views


urlpatterns = [

    path("", views.admin, name="statistics"),

    path('users/', views.UserListView.as_view(), name='users'),



    path('news/', views.update_list, {'content_type': 'NEWS'}, name='news'),
    path('news/create', views.update_form,{'content_type': 'NEWS'}, name='news_create'),
    path('news/<int:pk>/update', views.update_form,{'content_type': 'NEWS'}, name='news_update'),



    path('actions/', views.update_list, {'content_type': 'ACTION'}, name='actions'),
    path('action/create', views.update_form, {'content_type': 'ACTION'},name='action_create'),
    path('action/<int:pk>/update', views.update_form, {'content_type': 'ACTION'},name='action_update'),








    # можно ли совместить один маршрут для :
    # path('actions_lists/', views.update_list, {'content_type': 'ACTION'}, name='action_list'),
    # path('news_lists/', views.update_list, {'content_type': 'NEWS'}, name='news_lists'),


    path('movie/', views.movie_edit, name='movie'),

    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinemas/add', views.cinema_create, name='cinema_create'),
    path('cinemas/<int:pk>/update/', views.cinema_update, name='cinema_update'),
    path('cinema/<int:pk>/delete/', views.cinema_delete, name='cinema_delete'),

    path('cinemas/<int:pk>/hall_create/', views.hall_create, name='hall_create'),
    path('cinemas/<int:cinema_pk>/hall/<int:hall_pk>/update/', views.hall_update, name='hall_update'),
    path('cinemas/<int:cinema_pk>/hall/<int:hall_pk>/delete/', views.hall_delete, name='hall_delete'),




    # path('cinema/upload_gallery/', views.upload_gallery_image, name='upload_gallery_image') ,
    # path('cinema/add_hall/', views.cinema_create_hall, name='create_hall'),



    path('users/<int:pk>/edit/', views.edit_user, name='edit_user'),
    # path('test', views.test, name='test')

]


    #path('banners', views.banners, name="banners" ),]
#     path('films', views.films, name="films")
# ]