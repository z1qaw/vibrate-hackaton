from django.apps import AppConfig


class VibrateConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vibrate"

    def ready(self) -> None:
        from .models import Room

        for room in Room.objects.all():
            room.current_members.clear()
            room.save()
        return super().ready()
