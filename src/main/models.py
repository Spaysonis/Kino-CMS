from django.db import models
from src.cms.models.cinema import Movie, Hall, MovieFormat
from src.user.models import BaseUser as User
from datetime import time

class Schedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.TimeField(default=time(0, 0))
    price = models.FloatField(blank=True, null=True)
    format = models.ForeignKey(
        MovieFormat,
        on_delete=models.CASCADE,
        related_name="sessions",
        default=1
    )
    class Meta:
        unique_together = ("movie", "hall", "date", "time", "format")
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.movie.title} — {self.hall.name} — {self.date} {self.time} ({self.format})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    row = models.IntegerField()
    place = models.IntegerField()
