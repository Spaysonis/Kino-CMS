from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.cms'

    def ready(self):
        import src.cms.translation
        print('идет импорт -> import src.cms.translation ')

