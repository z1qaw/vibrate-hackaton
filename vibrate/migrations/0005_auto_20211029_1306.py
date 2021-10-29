# Generated by Django 3.2.8 on 2021-10-29 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vibrate', '0004_alter_room_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='current_members',
            field=models.ManyToManyField(null=True, related_name='room', to='vibrate.RoomMember'),
        ),
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.CharField(max_length=24, null=True, unique=True, verbose_name='Slug'),
        ),
    ]