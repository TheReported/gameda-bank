# Generated by Django 4.2.6 on 2023-11-04 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_bankaccount_alias'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BankAccount',
        ),
    ]