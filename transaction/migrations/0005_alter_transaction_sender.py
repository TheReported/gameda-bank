# Generated by Django 4.2.6 on 2023-11-11 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0015_remove_bankaccount_b_id_bankaccount_id'),
        ('transaction', '0004_alter_transaction_cac_alter_transaction_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='bank_account.bankaccount'),
        ),
    ]
