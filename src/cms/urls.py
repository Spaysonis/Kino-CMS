


from django.urls import path, include

from . import views
from src.cms import api_views
from .api_views import start_mailing
from ..decorators import staff_required

urlpatterns = [
    path('test', views.test, name='test'),
    path('test/admin/', views.test_admin, name='test_admin'),

    path("", staff_required(views.admin), name="statistics"),

    path('users/', staff_required(views.user_list), name='users'),
    path('users/<int:pk>/edit/', staff_required(views.edit_user), name='edit_user'),
    path('users/delete-user/<int:user_id>/', staff_required(api_views.api_delete_user), name='delete_user'),







    path('content/', staff_required(views.content_list), name='content_list'),
    path('content/create/<str:slug>/', staff_required(views.create_news_or_action), name='content_create'),
    path('content/update/<str:slug>/<int:pk>', staff_required(views.update_news_or_action), name='content_update'),
    path('content/delete/<int:pk>', staff_required(views.delete_news_or_action), name='delete_update'),
    path('pages', staff_required(views.pages), name='pages'),
    path('page/about/', staff_required(views.page_create), name='page_create'),
    path('page/home_edit/', staff_required(views.home_edit), name='home_edit'),
    path('page/contacts_edit/', staff_required(views.contacts_edit), name='contacts_edit'),




    path('banners/',staff_required( views.create_banners), name='banners'),
    path('background-banner/', staff_required(views.background_banner), name='background_banner'),



    path('movie/', staff_required(views.movies), name='movies'),
    path('movie/create', staff_required(views.movie_create_or_update), name='movie_create'),
    path('movie/<int:pk>/update',staff_required( views.movie_create_or_update), name='movie_update'),
    path('movie/<int:pk>/delete',staff_required( views.movie_delete), name='movie_delete'),



    path('cinemas/', staff_required(views.cinema_list), name='cinema_list'),
    path('cinemas/add',staff_required( views.cinema_create), name='cinema_create'),
    path('cinemas/<int:pk>/update/', staff_required(views.cinema_update), name='cinema_update'),
    path('cinema/<int:pk>/delete/', staff_required(views.cinema_delete), name='cinema_delete'),
    path('cinema/add_contact/',staff_required( views.add_contact), name='add_contact'),

    path('cinemas/<int:pk>/hall_create/', staff_required(views.hall_create), name='hall_create'),
    path('cinemas/<int:cinema_pk>/hall/<int:hall_pk>/update/', staff_required(views.hall_update), name='hall_update'),
    path('cinemas/<int:cinema_pk>/hall/<int:hall_pk>/delete/', staff_required(views.hall_delete), name='hall_delete'),


    path('mailing/', staff_required(views.mailing), name='mailing'),

    path('api/active-mailing/', staff_required(api_views.active_mailing), name='active_mailing'),
    path('api/upload-mailing/', staff_required(api_views.upload_mailing_api), name='upload_mailing_api'),
    path('api/delete-mailing/<int:mailing_id>/', staff_required(api_views.delete_mailing_api), name='delete_mailing_api'),
    path("api/start-mailing/", staff_required(start_mailing), name="start-mailing"),
    path("api/set_users/", staff_required(api_views.api_user_modal) , name="user_modal"),

















]
