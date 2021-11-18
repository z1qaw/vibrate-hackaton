import uuid

from django.contrib.auth import get_user_model, login
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import RoomCreateForm
from .models import Room, RoomMember
from .serializers import RoomMembersSerializer, RoomSerializer
from django.shortcuts import redirect

User = get_user_model()


def auto_login(function):
    def wrap_function(request, *args, **kwargs):
        if request.user.is_anonymous:
            new_user = User(username=uuid.uuid4().hex)
            new_user.save()
            request.user = new_user

            login(request, new_user)
        obj = function(request, *args, **kwargs)
        return obj
    return wrap_function


@auto_login
def index(request):
    return render(request, 'vibrate/index.html')


@auto_login
def rooms(request):
    return render(request, 'vibrate/rooms.html')


@auto_login
def room(request, room_slug):
    try:
        room_member = RoomMember.objects.get(user=request.user)
    except RoomMember.DoesNotExist:
        room_member = RoomMember(user=request.user)
        room_member.save()
    this_room = Room.objects.get(slug=room_slug)
    room_member = RoomMember.objects.get(user=request.user)
    return render(request, 'vibrate/room.html', {'room': this_room, 'room_user': room_member})


@auto_login
def create_room(request):
    room_member = RoomMember.objects.get(user=request.user)
    if request.method == "POST":
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = room_member
            room.save()
            return redirect('room_details', room_slug=room.slug)
    else:
        form = RoomCreateForm()
    return render(request, 'vibrate/create_room.html', {'form': form})


@api_view(['GET'])
def get_room_details(request, room_slug):
    return Response(RoomSerializer(Room.objects.get(slug=room_slug)).data)


@api_view(['GET'])
def get_room_members(request, room_slug):
    room = Room.objects.get(slug=room_slug)
    return Response(RoomMembersSerializer(room.current_members.all(), many=True).data)


@api_view(['GET'])
def get_rooms(request):
    room_member = RoomMember.objects.get(user=request.user)
    return Response(
        {
            'public': RoomSerializer(Room.objects.filter(is_private=False), many=True).data,
            'private': RoomSerializer(Room.objects.filter(is_private=True, owner_id=room_member.id), many=True).data
        }
    )



@api_view(['POST'])
def set_roommember_nickname(request):
    user = request.user
    roommember_of_user = RoomMember.objects.get(user=user)
    roommember_of_user.room_nickname = request.data['username']
    roommember_of_user.save()
    print('set nickname', request.data['username'])
    return Response(status=200)


@api_view(['GET'])
def get_me(request):
    user = request.user
    roommember_of_user = RoomMember.objects.get(user=user)
    return Response(RoomMembersSerializer(roommember_of_user).data)
