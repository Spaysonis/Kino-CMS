import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.cache import cache
HOLD = 30
class BookingConsumer(WebsocketConsumer):

    def connect(self):

        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.session_group_name = f"session_{self.session_id}"

        self.redis_key = self.session_id
        session_cache = cache.get(self.redis_key) or {}
        print('cache session ------ ',session_cache)



        async_to_sync(self.channel_layer.group_add)(
            self.session_group_name, self.channel_name
        )
        self.accept()



        print('Consumer ЗАКОНЕКТИЛСЯ фаил ------- consumer.py ')

    def receive(self, text_data):


        text_data_json = json.loads(text_data)

        client_id = text_data_json['client_id']
        row = text_data_json["row"]
        seat = text_data_json["seat"]
        redis_key = self.redis_key
        print(redis_key)


        session_cache = cache.get(redis_key) or {}


        if row not in session_cache:
            session_cache[row] = {}
        if seat in session_cache[row]:
            print('это место занято Client ' , client_id)
            return
        session_cache[row][seat] = client_id

        cache.set(redis_key, session_cache, timeout=HOLD)

        print(redis_key)
        print(session_cache)



        async_to_sync(self.channel_layer.group_send)(
            self.session_group_name, {"type": "chat.message", "message": text_data_json}
        )





    def chat_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({
            "type": "seat_update",
            "data": message
        }))