# Generated by Django 4.2.6 on 2023-11-07 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0013_alter_bankaccount_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='id',
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='b_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
