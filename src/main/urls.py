from django.urls import path

from . import views


urlpatterns = [
    path("", views.main_page, name="base_page"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('cinema/', views.cinema_list1, name='cinema_list1'),
]