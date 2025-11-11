from django.db import models

class Slider(models.Model):
    url = models.URLField(max_length=255)
    text = models.TextField(max_length=255, null=True, blank=True)
    image = models.ImageField()



class NewsPromoBanner(models.Model):
    is_active = models.BooleanField(default=True)
    slider = models.ManyToManyField(Slider)
    speed = models.IntegerField()



class HomepageBanner(models.Model):
    is_active = models.BooleanField(default=True)
    slider = models.ManyToManyField(Slider)
    speed = models.IntegerField()


class BackgroundBanner(models.Model):
    main_image = models.ImageField()
    background = models.CharField(max_length=7, default='#FFFFFF')
    is_use_image = models.BooleanField(default=False)

