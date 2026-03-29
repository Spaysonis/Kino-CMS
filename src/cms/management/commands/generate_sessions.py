import random
from datetime import time, timedelta
from django.core.management.base import BaseCommand
from src.cms.models import Hall, Movie
from src.main.models import Schedule


class Command(BaseCommand):
    help = 'Генерация полного расписания: каждый фильм в каждом зале каждый день'

    def handle(self, *args, **kwargs):
        halls = list(Hall.objects.all())
        movies = list(Movie.objects.all())

        if not halls or not movies:
            self.stdout.write(self.style.ERROR("Залы или фильмы не найдены!"))
            return

        # Определяем временную сетку (например, 6 сеансов в день для каждого зала)
        # Важно: время должно быть распределено так, чтобы сеансы не накладывались
        session_times = [
            time(9, 0), time(12, 0), time(15, 0),
            time(18, 0), time(21, 0), time(0, 0)
        ]

        # Собираем все уникальные дни проката из всех фильмов
        all_rental_days = set()
        for movie in movies:
            # Предполагаем, что rental_days() возвращает список объектов date
            all_rental_days.update(movie.rental_days())

        count = 0

        # Основной алгоритм:
        # Для каждого дня -> Для каждого зала -> Распределяем доступные фильмы по времени
        for day in sorted(all_rental_days):
            self.stdout.write(f"Обработка даты: {day}")

            for hall in halls:
                # Фильтруем фильмы, которые могут идти в этот конкретный день
                available_movies = [m for m in movies if day in m.rental_days()]

                if not available_movies:
                    continue

                # Перемешиваем фильмы для каждого зала, чтобы расписание было разнообразным
                random.shuffle(available_movies)

                # Берем доступные временные слоты и назначаем им фильмы
                for i, t in enumerate(session_times):
                    # Используем деление по модулю, чтобы если фильмов мало, они повторялись,
                    # а если много — чтобы заполнились все слоты времени.
                    movie = available_movies[i % len(available_movies)]

                    # Получаем доступные форматы для этого фильма
                    formats = list(movie.format_movie.all())
                    if not formats:
                        continue

                    fmt = random.choice(formats)

                    # Создаем сеанс (используем update_or_create, чтобы не дублировать при повторном запуске)
                    obj, created = Schedule.objects.get_or_create(
                        hall=hall,
                        date=day,
                        time=t,
                        defaults={
                            'movie': movie,
                            'format': fmt
                        }
                    )
                    if created:
                        count += 1

        self.stdout.write(self.style.SUCCESS(f"Успешно создано {count} новых сеансов!"))