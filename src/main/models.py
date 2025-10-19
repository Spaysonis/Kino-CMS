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


