from django.conf import settings
from django.db import models
from django.urls import reverse

from account.utils import ActiveManager, Status


class BankAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='accounts', on_delete=models.CASCADE
    )
    alias = models.CharField(max_length=40, blank=False, null=False)
    balance = models.DecimalField(decimal_places=2, default=0, max_digits=12)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)
    code = models.CharField(max_length=7, editable=False)

    objects = models.Manager()
    active = ActiveManager()

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
        self.code = f'A7-{self.id:04d}'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-balance']

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('bank_account:bank_account_detail', args=[self.code])
