from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'vibrate/index.html')


def rooms(request):
    return render(request, 'vibrate/rooms.html')
