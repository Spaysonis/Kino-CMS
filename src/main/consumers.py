# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer



class Send(WebsocketConsumer):
    print('runs wb')