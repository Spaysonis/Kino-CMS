


from django.urls import path

from . import views

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
]

    #path('banners', views.banners, name="banners" ),]
#     path('films', views.films, name="films")
# ]