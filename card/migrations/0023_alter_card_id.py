# Generated by Django 4.2.6 on 2023-11-07 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0022_card_code_alter_card_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
