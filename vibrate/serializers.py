from rest_framework import serializers
from .models import Room, RoomMember


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMember
        fields = '__all__'
