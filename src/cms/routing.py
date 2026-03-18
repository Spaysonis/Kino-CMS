from django.urls import re_path
from .consumers import MailingConsumer

websocket_urlpatterns = [
    re_path(r'ws/mailing/(?P<mailing_id>\d+)/$', MailingConsumer.as_asgi()),
]