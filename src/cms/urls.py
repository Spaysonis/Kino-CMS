

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views


urlpatterns = [

    path("", views.admin, name="statistics"),

    path('users/', views.UserListView.as_view(), name='users'),
    path('news/', views.news, name='news'),
    path('movie/', views.movie_edit, name='movie'),

    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinemas/add', views.cinema_create, name='cinema_create'),
    path('cinemas/<int:pk>/update/', views.cinema_update, name='cinema_update'),
    path('cinema/<int:pk>/delete/', views.cinema_delete, name='cinema_delete'),

    path('cinema/upload_gallery/', views.upload_gallery_image, name='upload_gallery_image') ,



    path('users/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('test', views.test, name='test')

]


    #path('banners', views.banners, name="banners" ),]
#     path('films', views.films, name="films")
# ]