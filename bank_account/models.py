from django.conf import settings
from django.db import models

from account.status import ACTIVE, CHOICES


class BankAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='accounts', on_delete=models.CASCADE
    )
    alias = models.CharField(max_length=40, blank=False, null=False)
    balance = models.DecimalField(decimal_places=2, default=0, max_digits=12)
    status = models.CharField(max_length=2, choices=CHOICES, default=ACTIVE)
    code = models.CharField(max_length=7, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
        self.code = f'A7-{self.id:04d}'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-balance']

    def __str__(self):
        return self.code
