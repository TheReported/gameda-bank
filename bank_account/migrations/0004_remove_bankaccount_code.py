# Generated by Django 4.2.6 on 2023-11-05 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0003_bankaccount_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='code',
        ),
    ]
