from src.cms.models import BackgroundBanner, HomePageBanner


def common_context(request):
    """Добавляет общие переменные во все шаблоны"""
    background_banner = BackgroundBanner.objects.first()
    banners = HomePageBanner.objects.filter(type_banner='TB')

    return {
        'background_banner': background_banner,
        'banners': banners,
    }