# Generated by Django 4.2.6 on 2023-11-16 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0027_remove_card_get_pin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='user',
        ),
    ]