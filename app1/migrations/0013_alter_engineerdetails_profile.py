# Generated by Django 4.2.2 on 2023-06-24 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_alter_engineerdetails_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engineerdetails',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app1.engineerprofile'),
        ),
    ]