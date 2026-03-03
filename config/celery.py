# config/celery.py
import os
from celery import Celery

# указываем путь к settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KinoCMS.config.settings")

# создаём объект Celery
app = Celery("KinoCMS")  # уникальное имя для проекта Celery

# читаем настройки Django, префикс CELERY_ будет использован
app.config_from_object("django.conf:settings", namespace="CELERY")

# автоматически ищем tasks.py во всех установленных приложениях
app.autodiscover_tasks()

