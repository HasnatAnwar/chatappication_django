"""
ASGI config for chatapplication project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import URLRouter , ProtocolTypeRouter
import chat.routing
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapplication.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket':
                URLRouter(
                    chat.routing.websocket_urlpatterns
        )
    }
)