
from django.db import models
from django.urls import reverse

from .gallery import Gallery
from phonenumber_field.modelfields import PhoneNumberField


class SeoBlock(models.Model):
    url = models.URLField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=200)
    key_words = models.CharField(max_length=200)
    description = models.TextField()






class Page(models.Model):
    PAGE_TYPES = (
        ('home', 'Главная страница'),
        ('about_cinema', 'О кинотеатре'),
        ('cafe_bar', 'Кафе - Бар'),
        ('vip', 'Vip-зал'),
        ('ads', 'Реклама'),
        ('kids_room', 'Детская комната'),
        ('contacts', 'Контакты'),
    )

    page_type = models.CharField(max_length=50, choices=PAGE_TYPES, unique=True)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    gallery = models.ManyToManyField(Gallery, blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    main_image = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    creation_data = models.DateTimeField(auto_now_add=True)

    def get_edit_url(self):
        if self.page_type == 'home':
            return reverse('home_edit')
        elif self.page_type == 'contacts':
            return reverse('contacts_edit')

        return f"{reverse('page_create')}?type={self.page_type}"

    @classmethod
    def active_pages(cls):
        return cls.objects.filter(is_active=True)


class HomePage:
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)
    phone1 = PhoneNumberField(blank=True, region='UA')
    phone2 = PhoneNumberField(blank=True, region='UA')


class Contact(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=255)
    main_image = models.ImageField()
    is_active = models.BooleanField(default=True)


class Updates(models.Model):
    class ContentType(models.TextChoices):
        NEWS = 'NEWS', 'Новости'
        ACTION = 'ACTION', 'Акции'

        @classmethod
        def from_slug(cls, slug):
            mapping = {
                'news':cls.NEWS,
                'action':cls.ACTION
            }
            return mapping.get(slug)

        @classmethod
        def to_slug(cls, enum_value):
            mapping = {
                cls.NEWS: 'news',
                cls.ACTION: 'action',
            }
            return mapping.get(enum_value, 'news')


    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    gallery = models.ManyToManyField(Gallery, blank=True)
    title = models.CharField(max_length=255, blank=True)
    publication_data = models.DateField()
    description = models.TextField(blank=True)
    main_image = models.ImageField()
    url = models.URLField(max_length=255)
    is_active = models.BooleanField(default=True)
    content_type = models.CharField(max_length=10, choices=ContentType.choices, default=ContentType.NEWS)



class MailTemplate(models.Model):
    file = models.FileField(upload_to='mailings/')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.file.name}"









class Product(models.Model):
    CATEGORY_CHOICES = [
        ('IZ', 'ИЖ'),
        ('JAVA', 'Ява'),
        ('URAL', 'Урал'),
        ('DNIPRO', 'Днепр'),
        ('PARTS', 'Запчасти'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'Доллар'),
        ('UAH', 'Гривна'),
    ]

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='IZ')
    name = models.CharField(max_length=255)
    article = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UAH')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)  # для теста

    def __str__(self):
        return f"{self.name} ({self.article})"
