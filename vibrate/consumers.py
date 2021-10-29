import json

# Импорты сторонних библиотек.
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# Импорты Django.
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from vibrate.views import room

# Локальные импорты.
from .models import Room, RoomMember
# from .utils import get_live_score_for_gameclass
from django.contrib.auth import get_user_model

User = get_user_model()


@sync_to_async
def get_user(username):
    return User.objects.get(username=username)


@sync_to_async
def get_room_member(user):
    return RoomMember.objects.get(user=user)


@sync_to_async
def get_room(room_slug):
    return Room.objects.get(slug=room_slug)


@sync_to_async
def join_member_to_room(member, room):
    return room.connect_user(member)


@sync_to_async
def leave_member_from_room(member, room):
    return room.disconnect_user(member)


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        username = self.scope['user']
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = 'room_' + self.room_slug
        user = await get_user(username)
        rm = await get_room_member(user)
        room = await get_room(self.room_slug)
        await join_member_to_room(rm, room)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_connect',
                'user_id': user.id,
                'room_slug': room.slug,
            }
        )

        await self.accept()

    async def disconnect(self, code):
        # Leave a room
        username = self.scope['user']
        user = await get_user(username)
        rm = await get_room_member(user)
        room = await get_room(self.room_slug)
        await leave_member_from_room(rm, room)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_disconnect',
                'user_id': user.id,
                'room_slug': room.slug,
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('disconnect', rm)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action_user = data['user_id']
        action = data['action']
        room_slug = data['room_slug']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'action',
                'user_id': action_user,
                'room_slug': room_slug,
                'action': action,
            }
        )

    async def action(self, event):
        action = event['action']
        user_id = event['user_id']

        await self.send(text_data=json.dumps(
            {
                'action': action,
                'user_id': user_id
            }
        ))
        print(event)

    async def user_disconnect(self, event):
        user_id = event['user_id']

        await self.send(text_data=json.dumps(
            {
                'action': 'user_disconnect',
                'user_id': user_id
            }
        ))

    async def user_connect(self, event):
        user_id = event['user_id']

        await self.send(text_data=json.dumps(
            {
                'action': 'user_connect',
                'user_id': user_id
            }
        ))
