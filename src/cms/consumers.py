from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class MailingConsumer(WebsocketConsumer):
    def connect(self):
        self.mailing_id = self.scope['url_route']['kwargs']['mailing_id']
        self.group_name = f"mailing_{self.mailing_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.accept()


    def mailing_progress(self, event):
        self.send(text_data=json.dumps({
            "status": "progress",
            "email": event.get("email"),
            "progress": event.get("progress")
        }))