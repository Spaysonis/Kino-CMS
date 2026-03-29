import os
import django # Добавьте это
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Сначала инициализируем Django
django_asgi_app = get_asgi_application()
django.setup() # Добавьте это ПЕРЕД вашими кастомными импортами

# Теперь импортируем всё остальное
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Импорты ваших маршрутов
from src.main.routing import websocket_urlpatterns as url_patterns_main
from src.chat.routing import websocket_urlpatterns as url_patterns_chat
from src.cms.routing import websocket_urlpatterns as url_pattern_mailing

all_websocket_patterns = url_patterns_chat + url_patterns_main + url_pattern_mailing


print("--- КАРТА ПУТЕЙ WEBSOCKET ---")
for pattern in all_websocket_patterns:
    print(f"Path: {pattern.pattern}")
print("----------------------------")


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(all_websocket_patterns))
        ),
    }
)
