import random

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import models
from django.urls import reverse

from account.utils import ActiveManager, Status
from bank_account.models import BankAccount

PIN_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Card(models.Model):
    bank_account = models.ForeignKey(
        BankAccount, related_name='cards_in_bank_account', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='total_cards', on_delete=models.CASCADE
    )
    alias = models.CharField(max_length=40, blank=False, null=False)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)
    pin = models.CharField(max_length=3, editable=False)
    get_pin = models.CharField(max_length=3, editable=False)
    code = models.CharField(max_length=7, editable=False)

    objects = models.Manager()
    active = ActiveManager()

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
        if not self.pin:
            self.get_pin = ''.join(random.choice(PIN_CHARS) for _ in range(3))
            self.pin = make_password(self.get_pin)
        self.code = f'C7-{self.id:04d}'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['alias']

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('card:detail', args=[self.code])
