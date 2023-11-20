# Generated by Django 4.2.6 on 2023-11-16 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0015_remove_bankaccount_b_id_bankaccount_id'),
        ('transaction', '0009_alter_transaction_sender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='cac',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account.bankaccount'),
        ),
    ]
