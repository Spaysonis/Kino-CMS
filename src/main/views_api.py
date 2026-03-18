from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from src.main.models import Schedule, Booking
import json
from django.http import JsonResponse
from django.core.cache import cache



def confirm_booking(request, pk):
    channel_layer = get_channel_layer()
    print('working api')
    data = json.loads(request.body)

    seats = data.get("seats")
    action = data.get("action")
    user = request.user
    print(user)
    redis_key = str(pk)
    session_cache = cache.get(redis_key) or {}

    for seat in seats:
        row = seat['row']
        place = seat['seat']
        Booking.objects.create(
            user=user,
            schedule_id=pk,
            row=row,
            place=place,
            booking_type = action
        )
        if row in session_cache and place in session_cache[row]:
            del session_cache[row][place]
            if not session_cache[row]:
                del session_cache[row]



        async_to_sync(channel_layer.group_send)(
            f"session_{pk}",
            {
                "type": "chat.message",
                "message": {
                    "action": "disable",
                    "row": row,
                    "seat": place
                }
            }
        )
    cache.set(redis_key, session_cache, timeout=30)
    return JsonResponse({"success": True})






def get_schedules_ajax(request, pk):

    selected_date = request.GET.get("date")
    selected_cinema = request.GET.get("cinema")
    selected_format = request.GET.get("format")


    print(selected_cinema)
    print(selected_date)
    print(selected_format)

    schedules = Schedule.objects.filter(movie_id=pk)

    if selected_date:
        parsed_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        schedules = schedules.filter(date=parsed_date)


    if selected_cinema:
        schedules = schedules.filter(hall__cinema_id=selected_cinema)


    if selected_format:
        schedules = schedules.filter(format__type=selected_format)

    schedules = schedules.select_related("hall", "format")
    data = [{
        "time": s.time.strftime("%H:%M"),
        "hall": s.hall.number,
        "format": s.format.type,
        "price": s.price or 0,
        "id":s.id


    }
        for s in schedules
    ]


    return JsonResponse({"schedules": data})