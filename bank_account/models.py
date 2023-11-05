from django.conf import settings
from django.db import models

from account.status import ACTIVE, CHOICES


class BankAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='accounts', on_delete=models.CASCADE
    )
    alias = models.CharField(max_length=40, blank=False, null=False)
    balance = models.DecimalField(decimal_places=2, default=0, max_digits=12)
    status = models.CharField(max_length=2, choices=CHOICES, default=ACTIVE)

    class Meta:
        ordering = ['-balance']

    @property
    def code(self):
        return f'A7-{self.id:04d}'

    def __str__(self):
        return self.code
