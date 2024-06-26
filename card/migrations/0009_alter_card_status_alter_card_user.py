# Generated by Django 4.2.6 on 2023-11-05 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0008_card_user_alter_card_bank_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(choices=[('AC', 'Active'), ('BL', 'Blocked'), ('DI', 'Discharge')], default='AC', max_length=2),
        ),
        migrations.AlterField(
            model_name='card',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards_has_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
