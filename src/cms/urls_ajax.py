from django.urls import path

from src.cms import views_ajax


urlpatterns = [
    path('cinema/<int:pk>/delete-image/<str:field>/',
         views_ajax.delete_cinema_image, name='cinema_delete_image'),

    path('cinema/<int:pk>/upload-image/<str:field>/',
         views_ajax.upload_cinema_image, name='cinema_upload_image')
]