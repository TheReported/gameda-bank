from django.db import models

from bank_account.models import BankAccount
from bank_account.utils import COMISSIONS, MovementKind


class Transaction(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    sender = models.CharField(max_length=7)
    cac = models.CharField(max_length=7)
    concept = models.TextField(max_length=200, blank=True, null=False)
    timeStamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    kind = models.CharField(
        max_length=3, choices=MovementKind.choices, default=MovementKind.OUTGOING
    )

    class Meta:
        ordering = ['-timeStamp']

    @property
    def commission(self):
        if 0 <= self.amount < 50:
            return self.amount * COMISSIONS[self.kind]["Tier1"] / 100
        elif 50 <= self.amount < 500:
            return self.amount * COMISSIONS[self.kind]["Tier2"] / 100
        elif self.amount >= 500:
            return self.amount * COMISSIONS[self.kind]["Tier3"] / 100

    def __str__(self):
        return self.sender
