# Generated by Django 4.2.6 on 2023-11-08 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_alter_transaction_options_alter_transaction_agent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='agent',
            new_name='cac',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='bank_account',
            new_name='sender',
        ),
    ]