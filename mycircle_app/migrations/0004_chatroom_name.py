# Generated by Django 5.0 on 2023-12-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycircle_app', '0003_alter_profile_friend_chatroom_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
