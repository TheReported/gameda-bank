from django.db import models

from bank_account.utils import COMISSIONS
from card.models import Card

PAYMENT_KIND = 'PAY'


class Payment(models.Model):
    business = models.CharField(max_length=30, blank=True, default='Gift')
    ccc = models.ForeignKey(Card, related_name='payments_card', on_delete=models.CASCADE)
    pin = models.CharField(max_length=3, blank=False, null=False)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    @property
    def commission(self):
        if 0 <= self.amount < 50:
            return self.amount * COMISSIONS[PAYMENT_KIND]["Tier1"] / 100
        elif 50 <= self.amount < 500:
            return self.amount * COMISSIONS[PAYMENT_KIND]["Tier2"] / 100
        elif self.amount >= 500:
            return self.amount * COMISSIONS[PAYMENT_KIND]["Tier3"] / 100

    def __str__(self):
        return self.business
