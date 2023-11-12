# Generated by Django 4.2.6 on 2023-11-11 19:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('card', '0026_alter_card_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0002_alter_payment_options_payment_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='total_payments',
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='ccc',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='payments_card',
                to='card.card',
            ),
        ),
    ]
