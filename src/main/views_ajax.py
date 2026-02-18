from django.http import JsonResponse
from datetime import datetime
from src.main.models import Schedule



def get_schedules_ajax(request, pk):

    selected_date = request.GET.get("date")
    selected_cinema = request.GET.get("cinema")
    format_movie = request.GET.get("format")

    print(selected_cinema)
    print(selected_date)
    print(format_movie)

    schedules = Schedule.objects.filter(movie_id=pk)

    if selected_date:
        parsed_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        schedules = schedules.filter(date=parsed_date)

    if selected_cinema:
        schedules = schedules.filter(hall__cinema_id=selected_cinema)

    schedules = schedules.select_related("hall", "format")
    data = [{
            "time": s.time.strftime("%H:%M"),
            "hall": s.hall.number,
            "format": s.format.type,
            "price": s.price,
    }
        for s in schedules
    ]

    return JsonResponse({"schedules": data})