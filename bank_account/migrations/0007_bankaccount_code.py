# Generated by Django 4.2.6 on 2023-11-05 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0006_remove_bankaccount_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='code',
            field=models.CharField(default='A7-0004', editable=False, max_length=7),
            preserve_default=False,
        ),
    ]
