from django.db import models
from django.urls import reverse

from account.utils import ActiveManager, Status
from bank_account.models import BankAccount


class Card(models.Model):
    bank_account = models.ForeignKey(BankAccount, related_name='cards', on_delete=models.CASCADE)
    alias = models.CharField(max_length=40, blank=False, null=False)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)
    pin = models.CharField(max_length=3, editable=False)
    code = models.CharField(max_length=7, editable=False)

    objects = models.Manager()
    active = ActiveManager()

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
        self.code = f'C7-{self.id:04d}'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['alias']

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('card:detail', args=[self.code])
