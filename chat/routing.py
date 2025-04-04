# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/(?P<token>\w+)", consumers.ChatConsumer.as_asgi()),
]