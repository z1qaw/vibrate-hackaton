from django.forms import ModelForm
from .models import Room


class RoomCreateForm(ModelForm):
     class Meta:
        model = Room
        exclude = ['owner', 'slug', 'current_members']