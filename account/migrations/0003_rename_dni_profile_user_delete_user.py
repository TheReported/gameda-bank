# Generated by Django 4.2.6 on 2023-10-27 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_rename_user_profile_dni_profile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='dni',
            new_name='user',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
