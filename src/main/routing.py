from django.urls import re_path
from src.main import consumers
from django.urls import path


websocket_urlpatterns = [
path("ws/booking/session/<int:session_id>/", consumers.BookingConsumer.as_asgi()),

]
