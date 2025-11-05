
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField



class BaseUser(AbstractUser):
    nick_name = models.CharField(max_length=100, blank=True, default='')  # ← blank=True
    address = models.CharField(max_length=200, blank=True, default='')    # ← blank=True
    card_num = models.CharField(max_length=19, blank=True, default='')
    language = models.CharField(max_length=100, blank=True, default='ru') # ← default value
    gender = models.CharField(max_length=100, blank=True, default='')
    date_of_birth = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    phone_num = PhoneNumberField(blank=True, region='UA', default='')




