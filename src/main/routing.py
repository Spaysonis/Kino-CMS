from django.urls import re_path
from src.main import consumers



websocket_urlpatterns = [
    re_path(r'ws/booking/session/(?P<session_id>\d+)/?$', consumers.BookingConsumer.as_asgi()),

]