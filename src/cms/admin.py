from django.contrib import admin
from django.apps import apps

# Регистриую все модели
for model in apps.get_app_config('cms').get_models():
    admin.site.register(model)