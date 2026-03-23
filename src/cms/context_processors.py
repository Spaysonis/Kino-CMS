from src.cms.models.page import Page
def pages_processor(request):
    return {
        "sidebar_pages": Page.objects.all()
    }