# Generated by Django 4.2.6 on 2023-11-03 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_rename_bank_account_id_bankaccount_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='alias',
            field=models.CharField(max_length=40),
        ),
    ]
