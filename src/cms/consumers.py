from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.core.cache import cache

class MailingConsumer(WebsocketConsumer):
    def connect(self):
        self.mailing_id = self.scope['url_route']['kwargs']['mailing_id']
        self.group_name = f"mailing_{self.mailing_id}"

        # Подключаю ВБ к группе рассылки
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.accept()

        #  Отправляю сразу текущий прогресс после подключения
        progress = cache.get(f"mailing:{self.mailing_id}:progress")
        meta = cache.get(f"mailing:{self.mailing_id}:meta")


        if progress:
            self.send(text_data=json.dumps({
                "status": "progress",
                "sent": progress,
                "meta": meta,

                "progress": int(progress["sent"] / progress["total"] * 100) if progress["total"] else 0
            }))



    def mailing_progress(self, event):
        self.send(text_data=json.dumps({
            "status": "progress",
            "email": event.get("email"),
            "progress": event.get("progress"),
            'backend':'backend'
        }))



    def mailing_finished(self, event):
        self.send(text_data=json.dumps({
            "status": "finished",
            "total": event.get("total")
        }))