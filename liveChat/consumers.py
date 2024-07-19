from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['user'].id
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']

        # Generate a unique room name based on the user IDs
        self.room_name = self.get_room_name(self.sender_id, self.recipient_id)
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user']

        sender = await self.get_user(user_id)
        recipient = await self.get_user(self.recipient_id)

        await self.save_message(sender, recipient, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @sync_to_async
    def save_message(self, sender, recipient, message):
        ChatMessage.objects.create(sender=sender, recipient=recipient, message=message)

    def get_room_name(self, user1_id, user2_id):
        return f'room_{min(user1_id, user2_id)}_{max(user1_id, user2_id)}'
