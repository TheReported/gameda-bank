from django.conf import settings
from django.db import models

from card.models import Card


class Payment(models.Model):
    business = models.CharField(max_length=30, blank=True, default='Gift')
    ccc = models.ForeignKey(Card, related_name='payments_card', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='total_payments', on_delete=models.CASCADE
    )
    pin = models.CharField(max_length=3, blank=False, null=False)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.business
