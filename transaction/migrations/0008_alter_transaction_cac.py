# Generated by Django 4.2.6 on 2023-11-11 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_transaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='cac',
            field=models.CharField(max_length=7),
        ),
    ]
