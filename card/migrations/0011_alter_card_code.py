# Generated by Django 4.2.6 on 2023-11-05 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0010_alter_card_options_card_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='code',
            field=models.CharField(editable=False, max_length=7),
        ),
    ]
