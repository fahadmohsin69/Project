# Generated by Django 4.2.2 on 2023-06-24 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0009_engineerprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='userProfile',
        ),
        migrations.AlterField(
            model_name='engineerdetails',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app1.engineerprofile'),
        ),
    ]
