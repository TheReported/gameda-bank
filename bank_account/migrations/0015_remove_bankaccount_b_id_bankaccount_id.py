# Generated by Django 4.2.6 on 2023-11-07 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0014_remove_bankaccount_id_bankaccount_b_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='b_id',
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='id',
            field=models.BigAutoField(auto_created=True, default=3, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
