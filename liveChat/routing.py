# messaging/routing.py

from django.urls import path
from liveChat.consumers import ChatConsumer

# Define the websocket urls
websocket_urlpatterns = [
    path('ws/chat/<int:recipient_id>/', ChatConsumer.as_asgi()),
]
