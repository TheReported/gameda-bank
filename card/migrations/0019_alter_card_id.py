# Generated by Django 4.2.6 on 2023-11-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0018_card_code_alter_card_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]