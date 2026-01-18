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

    is_active = models.BooleanField(default=False)
    type_banner = models.CharField(max_length=2 , choices=BANNER_CHOICE, default=TOP_BANNER)
    speed = models.IntegerField(default=5, null=True, blank=True)
    slider = models.ManyToManyField(Slider)


class BackgroundBanner(models.Model):
    main_image = models.ImageField(blank=True)
    background = models.CharField(max_length=7, default='#FFFFFF')
    is_use_image = models.BooleanField(default=False)





# class Banner(models.Model):
#     TOP = 'TP'
#     NEWS = 'NB'
#
#     TYPE_CHOICES = [
#         (TOP, 'Top banner'),
#         (NEWS, 'News banner'),
#     ]
#
#     type_banner = models.CharField(max_length=2, choices=TYPE_CHOICES, unique=True)
#     is_active = models.BooleanField(default=True)
#     speed_rotation = models.IntegerField(default=5)
#
#
# class Slide(models.Model):
#     banner = models.ForeignKey(
#         Banner,
#         related_name='slides',
#         on_delete=models.CASCADE
#     )
#
#     url = models.URLField(max_length=255)
#     text = models.TextField(max_length=255, null=True, blank=True)
#     image = models.ImageField()





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
