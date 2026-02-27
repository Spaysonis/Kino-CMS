import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.cache import cache

from src.main.models import Booking

HOLD = 30
class BookingConsumer(WebsocketConsumer):

    def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.session_group_name = f"session_{self.session_id}"
        self.redis_key = self.session_id

        async_to_sync(self.channel_layer.group_add)(
            self.session_group_name, self.channel_name
        )




        self.accept()
        seat_events = []

        booked_seats = Booking.objects.filter(
            schedule_id=self.session_id
        ).values("row", "place")


        session_cache = cache.get(self.redis_key) or {}

        if session_cache:
            for row, seats in session_cache.items():
                for seat, client in seats.items():
                    seat_events.append({
                        "action": "booking",
                        "client_id": client,
                        "row": row,
                        "seat": seat,
                    })



        print('session cache on connect',session_cache)
        self.send(text_data=json.dumps({
            "type": "init_seats",
            "data": seat_events
        }))


        print('Consumer ЗАКОНЕКТИЛСЯ фаил ------- consumer.py ')

    def receive(self, text_data):

        data_with_frontend = json.loads(text_data)

        client_id = data_with_frontend['client_id']
        row = data_with_frontend["row"]
        seat = data_with_frontend["seat"]
        action = data_with_frontend["action"]
        redis_key = self.redis_key

        session_cache = cache.get(redis_key) or {}

        if action == 'booking':
            if row not in session_cache:
                session_cache[row] = {}
            if seat in session_cache[row]:
                print('место уже занято')
                return
            session_cache[row][seat] = client_id

            print('я добавил забронировал место для ', client_id)

        elif action == 'cancel':
            if row in session_cache and seat in session_cache[row]:

                if session_cache[row][seat] == client_id:
                    del session_cache[row][seat]
                    if not session_cache[row]:
                        del session_cache[row]
        cache.set(redis_key, session_cache, timeout=HOLD)

        async_to_sync(self.channel_layer.group_send)(
            self.session_group_name, {"type": "chat.message", "message": data_with_frontend}
        )





    def chat_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({
            "type": "seat_update",
            "data": message
        }))