from datetime import time

from django.core.management.base import BaseCommand

from src.cms.models import Hall, Movie
from src.main.models import Schedule


class Command(BaseCommand):
    help = "Создаёт сеансы для всех фильмов и всех доступных залов"

    def handle(self, *args, **kwargs):
        halls = Hall.objects.all()  # все залы
        times = [time(10, 0), time(14, 0), time(18, 0), time(21, 0)]

        for movie in Movie.objects.all():
            if not movie.start_date or not movie.end_date:
                continue
            days = movie.rental_days()
            formats = movie.format_movie.all()

            for day in days:
                for hall in halls:
                    for t in times:
                        for fmt in formats:
                            Schedule.objects.get_or_create(
                                movie=movie,
                                hall=hall,
                                date=day,
                                time=t,
                                format=fmt
                            )
        self.stdout.write(self.style.SUCCESS("Сеансы для всех залов успешно созданы!"))