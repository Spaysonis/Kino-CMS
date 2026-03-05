"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


from src.main.routing import websocket_urlpatterns as url_patterns_main
from src.chat.routing import websocket_urlpatterns as url_patterns_chat
from src.cms.routing import websocket_urlpatterns as url_pattern_mailing
all_websocket_patterns =  url_patterns_chat + url_patterns_main + url_pattern_mailing


django_asgi_app = get_asgi_application()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')



application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(all_websocket_patterns))
        ),
    }
)