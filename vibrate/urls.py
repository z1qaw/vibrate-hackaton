from django.urls import path

from .views import (get_room_details, get_room_members, get_rooms, 
                    index, room, rooms, set_roommember_nickname, get_me, create_room)

urlpatterns = [
    path('rooms', rooms),
    path('room/<str:room_slug>', room, name='room_details'),
    path('create-room', create_room),

    path('api/get_rooms', get_rooms),
    path('api/get_room_details/<str:room_slug>/', get_room_details),
    path('api/get_room_members/<str:room_slug>/', get_room_members),
    path('api/set_roommember_nickname/', set_roommember_nickname),
    path('api/get_me/', get_me),

    path('', index),
]
