
from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class BaseUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('ua', 'Украинский'),
    ]

    nick_name = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=200, blank=True, default='')
    card_num = models.CharField(max_length=19, blank=True, default='')
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, default='ru')
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, default='')
    date_of_birth = models.DateField( blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, default='')
    phone_num = PhoneNumberField(blank=True, region='UA', default='')




