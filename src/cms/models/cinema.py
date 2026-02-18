from datetime import timedelta, time
from django.db import models
from .page import SeoBlock
from .gallery import Gallery



class Cinema(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)  # Удалит связаны обькт models.CASCADE
    gallery = models.ManyToManyField(Gallery, blank=True)

    title = models.CharField(max_length=100 ,blank=True)
    description = models.TextField(blank=True)
    main_image = models.ImageField()
    conditions = models.TextField(blank=True, null=True)
    image_top_banner = models.ImageField()
    address = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=255)




class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE,blank=True, null=True)
    gallery = models.ManyToManyField(Gallery)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, blank=True, null=True)

    number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    scheme_image = models.ImageField(blank=True, null=True)
    top_banner_image = models.ImageField(blank=True, null=True)
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_default = models.BooleanField(default=False) # Для дефолтнго зала Если false - то могу удаялть





class MovieFormat(models.Model):

    class FormatType(models.TextChoices):
        Format = "2D", "2D"
        THREE_D = "3D", "3D"
        IMAX = "IMAX", "IMAX"


    type = models.CharField(
        max_length=10,
        choices=FormatType.choices,
        unique=True
    )

    def __str__(self):
        return self.type



class Movie(models.Model):





    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, blank=True, null=True)
    gallery = models.ManyToManyField(Gallery, blank=True)

    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    main_image = models.ImageField()
    url = models.URLField(max_length=255)

    format_movie =models.ManyToManyField(
        MovieFormat,
        related_name="movies",
        blank=True
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


    def rental_days(self):
        """
        This fun makes list on the data rental
        """

        if not self.start_date and not self.end_date:
            return []
        days = []
        current = self.start_date
        while current <= self.end_date:
            days.append(current)
            current += timedelta(days=1)
        return days


    # def demo_sessions(self):
    #
    #     sessions = {}
    #
    #     for day in self.rental_days():
    #         sessions[day] = [
    #             time(10, 0),
    #             time(13, 30),
    #             time(16, 0),
    #             time(19, 45),
    #             time(22, 0),
    #         ]
    #
    #     return sessions






