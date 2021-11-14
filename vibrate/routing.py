from django.urls import path

from .consumers import RoomConsumer

websocket_urlpatterns = [
    path('ws/room/<str:room_slug>/', RoomConsumer.as_asgi())
]
