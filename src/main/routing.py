from django.urls import path
from src.main.consumers import Send
websocket_urlpatterns = [
    path("ws/booking/session/<int:DateSession>/<int:seat>/<int:row>",Send.as_asgi())
    ]