from django.urls import path
from django.urls.conf import include
from .views import index, rooms


urlpatterns = [
    path('rooms', rooms),
    path('', index),
]
