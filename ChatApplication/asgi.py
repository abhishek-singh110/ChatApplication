"""
ASGI config for ChatApplication project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import liveChat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApplication.settings')

# Configure the ASGI Server
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
           liveChat.routing.websocket_urlpatterns
        )
    ),
})
