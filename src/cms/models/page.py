from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from .gallery import Gallery
from phonenumber_field.modelfields import PhoneNumberField


class SeoBlock(models.Model):
    url = models.URLField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=200)
    key_words = models.CharField(max_length=200)
    description = models.TextField()






class Page(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)
    gallery = models.ManyToManyField(Gallery)

    tittle = models.CharField(max_length=200)
    description = models.TextField()
    main_image = models.ImageField()
    is_active = models.BooleanField(default=False)
    creation_data = models.DateTimeField()


class HomePage:
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)
    phone1 = PhoneNumberField(blank=True, region='UA')
    phone2 = PhoneNumberField(blank=True, region='UA')


class Contact(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)
    tittle = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=255)
    main_image = models.ImageField()



class Updates(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('NEWS', 'Новости'),
        ('ACTION', 'Акции'),
    ]

    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    gallery = models.ManyToManyField(Gallery, blank=True)
    title = models.CharField(max_length=255)
    publication_data = models.DateTimeField()
    description = models.TextField()
    main_image = models.ImageField()
    url = models.URLField(max_length=255)
    is_active = models.BooleanField(default=True)
    content_type = models.CharField(max_length=10, choices=
                                    CONTENT_TYPE_CHOICES, default='NEWS')



class Mailing(models.Model):
    file = models.FileField()
