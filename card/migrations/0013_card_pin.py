# Generated by Django 4.2.6 on 2023-11-06 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0012_alter_card_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='pin',
            field=models.CharField(default='YHM', editable=False, max_length=3),
        ),
    ]
