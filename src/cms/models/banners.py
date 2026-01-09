from django.db import models


class Slider(models.Model):
    url = models.URLField(max_length=255)
    text = models.TextField(max_length=255, null=True, blank=True)
    image = models.ImageField()





class HomePageBanner(models.Model):
    TOP_BANNER = 'TB'
    NEWS_BANNER = 'NB'

    BANNER_CHOICE =[
        (TOP_BANNER, 'На главной вверх'),
        (NEWS_BANNER, 'На главной новости и акции')
    ]

    is_active = models.BooleanField(default=True)
    type_banner = models.CharField(max_length=2 , choices=BANNER_CHOICE, default=TOP_BANNER)
    speed = models.IntegerField(default=5)
    slider = models.ManyToManyField(Slider)






class BackgroundBanner(models.Model):
    main_image = models.ImageField()
    background = models.CharField(max_length=7, default='#FFFFFF')
    is_use_image = models.BooleanField(default=True)




#
# class NewsPromoBanner(models.Model):
#     is_active = models.BooleanField(default=True)
#     speed = models.IntegerField()
#     slider = models.ManyToManyField(Slider)


#
# class HomepageBanner(models.Model):
#     is_active = models.BooleanField(default=True)
#     speed = models.IntegerField()
#     slider = models.ManyToManyField(Slider)
