from django.contrib import admin

from .models import Booking, Schedule

admin.site.register(Schedule)
admin.site.register(Booking)