# Generated by Django 4.2 on 2023-07-05 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_topic_room_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engineerdetails',
            name='address',
        ),
        migrations.RemoveField(
            model_name='engineerdetails',
            name='country',
        ),
        migrations.AddField(
            model_name='engineerprofile',
            name='is_engineer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_user',
            field=models.BooleanField(default=False),
        ),
    ]
