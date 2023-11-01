from django.conf import settings
from django.db import models


class Status(models.TextChoices):
    ACTIVE = 'AC', 'Active'
    BLOCKED = 'BL', 'Blocked'
    DISCHARGE = 'DI', 'Discharge'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)


class BankAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.TextField(max_length=7, default='A1-0001', blank=False, null=False)
    alias = models.TextField(max_length=40, blank=False, null=False)
    balance = models.DecimalField(decimal_places=2, default=0, max_digits=12)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)
