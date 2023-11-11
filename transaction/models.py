from django.db import models

from bank_account.models import BankAccount


class Transaction(models.Model):
    class Kind(models.TextChoices):
        OUTGOING = 'OUT', 'Outgoing'
        INCOMING = 'INC', 'Incoming'

    sender = models.ForeignKey(
        BankAccount, related_name='sender_transactions', on_delete=models.CASCADE
    )
    cac = models.ForeignKey(BankAccount, related_name='cac', on_delete=models.CASCADE)
    concept = models.TextField(max_length=200, blank=True, null=False)
    timeStamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    kind = models.CharField(max_length=3, choices=Kind.choices, default=Kind.OUTGOING)

    class Meta:
        ordering = ['-timeStamp']

    def __str__(self):
        return self.sender