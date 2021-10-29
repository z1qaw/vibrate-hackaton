# Generated by Django 3.2.8 on 2021-10-28 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_nickname', models.CharField(max_length=255, verbose_name='Nickname')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is room active')),
                ('current_members', models.ManyToManyField(related_name='room', to='vibrate.RoomMember')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_room', to='vibrate.roommember')),
            ],
        ),
    ]