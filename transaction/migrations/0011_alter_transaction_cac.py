# Generated by Django 4.2.6 on 2023-11-20 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0010_remove_transaction_user_alter_transaction_cac'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='cac',
            field=models.CharField(max_length=7),
        ),
    ]