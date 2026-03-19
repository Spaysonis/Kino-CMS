import random
from datetime import time

from django.core.management.base import BaseCommand

from src.cms.models import Hall, Movie
from src.main.models import Schedule


class Command(BaseCommand):
    help = 'sessions list'

    def handle(self, *args, **kwargs):
        halls = list(Hall.objects.all())
        movies = list(Movie.objects.all())

        times = [time(10, 0), time(14, 0), time(18, 0), time(21, 0)]

        # собираем все дни проката
        all_days = set()
        for movie in movies:
            all_days.update(movie.rental_days())

        for day in sorted(all_days):
            for t in times:
                random.shuffle(movies)  # перемешиваем фильмы

                for i, hall in enumerate(halls):
                    if i >= len(movies):
                        break

                    movie = movies[i]

                    # берем случайный формат фильма
                    formats = list(movie.format_movie.all())
                    if not formats:
                        continue

                    fmt = random.choice(formats)

                    # проверка на занятость зала
                    if Schedule.objects.filter(hall=hall, date=day, time=t).exists():
                        continue

                    Schedule.objects.create(
                        movie=movie,
                        hall=hall,
                        date=day,
                        time=t,
                        format=fmt
                    )

        self.stdout.write(self.style.SUCCESS("Расписание успешно сгенерировано!"))