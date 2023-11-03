import random

from django.conf import settings
from django.db import models

from account.status import ACTIVE, CHOICES


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='cards', on_delete=models.CASCADE
    )
    alias = models.TextField(max_length=40, blank=False, null=False)
    status = models.CharField(max_length=2, choices=CHOICES, default=ACTIVE)
    pin = models.CharField(max_length=3)

    def save(self, *args, **kwargs):
        find_last = Card.objects.filter(user=self.user).order_by("-id").first()
        if find_last:
            last_number = int(find_last.id) + 1
        else:
            last_number = 1
        self.code = f"C7-{last_number:04d}"
        self.pin = ''.join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(3))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.alias
