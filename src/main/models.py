from django.db import models
from src.cms.models.cinema import Movie, Hall, MovieFormat
from src.user.models import BaseUser as User



class Visitor(models.Model):
    DEVICE_CHOICES = [
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('desktop', 'Desktop'),
        ('other', 'Other'),
    ]
    session_key = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.device_type} — {self.created_at.date()}"



class Schedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="schedules")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
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
        return f"{self.movie.title} — {self.hall.number} — {self.date} {self.time} ({self.format})"


class Booking(models.Model):
    class BookingType(models.TextChoices):
        BOOKING = "booking", "Бронь"
        PURCHASE = "purchase", "Покупка"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    row = models.IntegerField()
    place = models.IntegerField()
    booking_type = models.CharField(
        max_length=10,
        choices=BookingType.choices,
        default=BookingType.BOOKING
    )


