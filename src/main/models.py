from django.db import models
from src.cms.models.cinema import Movie, Hall
from src.user.models import BaseUser as User


class Schedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    data = models.DateTimeField()
    price = models.FloatField()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    row = models.IntegerField()
    place = models.IntegerField()
