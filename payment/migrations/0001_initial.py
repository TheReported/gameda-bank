# Generated by Django 4.2.6 on 2023-11-05 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('card', '0009_alter_card_status_alter_card_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.CharField(blank=True, default='Gift', max_length=30)),
                ('pin', models.CharField(max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('ccc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ccc', to='card.card')),
            ],
        ),
    ]
