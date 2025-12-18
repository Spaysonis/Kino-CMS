from django.db import models
from .page import SeoBlock
from .gallery import Gallery



class Cinema(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)  # Удалит связаны обькт models.CASCADE
    gallery = models.ManyToManyField(Gallery, blank=True)

    title = models.CharField(max_length=100)
    description = models.TextField()
    main_image = models.ImageField()
    conditions = models.TextField(blank=True, null=True)
    image_top_banner = models.ImageField()
    address = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=255)




class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE,blank=True, null=True)
    gallery = models.ManyToManyField(Gallery, null=True)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, blank=True, null=True)

    number = models.CharField(max_length=100)
    description = models.TextField()
    scheme_image = models.ImageField(blank=True, null=True)
    top_banner_image = models.ImageField(blank=True, null=True)
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )


class Movie(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)
    gallery = models.ManyToManyField(Gallery)

    title = models.CharField(max_length=100)
    description = models.TextField()
    main_image = models.ImageField()
    url = models.URLField(max_length=255)
    format_3d = models.BooleanField(default=False)
    format_2d = models.BooleanField(default=False)
    format_imax = models.BooleanField(default=False)



