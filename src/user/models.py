
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField



class BaseUser(AbstractUser):
    nick_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    card_num = models.CharField(max_length=19, blank=True)
    language = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_num = PhoneNumberField(blank=True, region='UA')




