# Generated by Django 4.2.2 on 2023-07-06 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_rename_user_userprofile_userr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='userr',
            new_name='user',
        ),
    ]
