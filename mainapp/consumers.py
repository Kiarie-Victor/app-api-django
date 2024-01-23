from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timesince import timesince
from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope['user'] = await self.get_user(scope=scope)
        return super().__call__(scope, receive,send)

    @sync_to_async
    def get_user(self, scope):
        if 'user' in scope:
            return scope['user']
        return None

class ChatConsumer(AsyncWebsocketConsumer):


    # WebSocket Connection handling
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' %self.room_name
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # Handling WebSocket Disconnection

    async def disconnect(self, text_content):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def fetch_messages(self, data):
        content = {
            'command': 'fetch_messages',
            'messages': self.messages_to_json(data)
        }
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    def message_to_json(self, message):
        return {
            'author': message.sender.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    # Handling message receiving
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']
        message = data['message']

        if action == "one-to-one":
            # handling one-to-one chat messages
            pass
        elif action == "group":
            pass


