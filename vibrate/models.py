from typing import ForwardRef
from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()


class RoomMember(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room_nickname = models.CharField('Nickname', max_length=255)


class Room(models.Model):
    owner = models.ForeignKey(
        to=RoomMember, on_delete=models.CASCADE, related_name='owned_room')
    name = models.CharField('Название', max_length=255)
    current_members = models.ManyToManyField(
        to=RoomMember, related_name='room', blank=True)
    slug = models.CharField('Slug', max_length=24, unique=True, null=True)
    is_private = models.BooleanField('Сделать комнату приватной', default=False)

    def save(self, *args, **kwargs):
        try:
            a = self.slug
            if not self.slug:
                self.slug = uuid.uuid4().hex
        except:
            self.slug = uuid.uuid4().hex
        super(Room, self).save(*args, **kwargs)

    def connect_user(self, user):
        is_user_added = False
        if not user in self.current_members.all():
            self.current_members.add(user)
            self.save()
            is_user_added = True
        elif user in self.current_members.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        is_user_removed = False
        if user in self.current_members.all():
            self.current_members.remove(user)
            self.save()
            is_user_removed = True
        elif not user in self.current_members.all():
            is_user_removed = True
        return is_user_removed
