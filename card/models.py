import random

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import models

from account.status import ACTIVE, CHOICES

PIN_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='cards', on_delete=models.CASCADE
    )
    alias = models.CharField(max_length=40, blank=False, null=False)
    status = models.CharField(max_length=2, choices=CHOICES, default=ACTIVE)

    @property
    def pin(self):
        return make_password(''.join(random.choice(PIN_CHARS) for _ in range(3)))

    @property
    def code(self):
        return f"C7-{self.id:04d}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.alias
