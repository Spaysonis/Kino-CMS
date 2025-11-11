


from django.urls import path

from . import views

urlpatterns = [

    path("", views.admin, name="statistics"),

    path('users/', views.get_user_info, name='users'),
    path('news/', views.news, name='news'),
    path('movie', views.movie_edit, name='movie')

]

    #path('banners', views.banners, name="banners" ),]
#     path('films', views.films, name="films")
# ]