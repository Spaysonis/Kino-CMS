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
    is_draft = models.BooleanField(default=True)



class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    gallery = models.ManyToManyField(Gallery)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)

    number = models.CharField(max_length=100)
    description = models.TextField()
    scheme_image = models.ImageField()
    top_banner_image = models.ImageField()


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



