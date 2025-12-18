from django.db import models


class Gallery(models.Model):
    image = models.ImageField(blank=True)
