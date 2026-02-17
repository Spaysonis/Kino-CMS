from modeltranslation.translator import register, TranslationOptions

from src.cms.models import Updates
from src.cms.models.cinema import Cinema, Hall, Movie


@register(Cinema) # декоратор register - регистрирует моедь Cinema в modeltranslation и свзязывает настройки с TranslationOptions
class CinemaTranslation(TranslationOptions): # говорю TranslationOptions какие поля нужно переводить
    # TranslationOptions - создаст в бд автоматически поля с ru - en для филдов которые я передам
    fields = ('title', 'description')


@register(Hall)
class HallTranslation(TranslationOptions):
    fields = ('number', 'description')


@register(Updates)
class UpdateTranslation(TranslationOptions):
    fields = ('title', 'description')


@register(Movie)
class MovieTranslation(TranslationOptions):
    fields = ('title', 'description')

