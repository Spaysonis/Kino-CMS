from django.db.models.signals import post_migrate
from django.dispatch import receiver
from src.cms.models.page import Page, Contact


@receiver(post_migrate)
def create_default_pages(sender, **kwargs):
    print(' сработал! ------------------')
    for page_type, _ in Page.PAGE_TYPES:
        Page.objects.get_or_create(page_type=page_type)


@receiver(post_migrate)
def create_initial_contact(sender, **kwargs):
    print('post_migrate сработал для', sender.name)
    if sender.name == 'src.cms':
        print('Создаём первую запись Contact для =====', sender.name)
        if not Contact.objects.exists():
            Contact.objects.create(
                title='Названеие кинотеатра',
                address='',
                coordinates='',
                main_image=None,
                is_active=True
            )