from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Status.ACTIVE)


class Status(models.TextChoices):
    ACTIVE = 'AC', 'Active'
    BLOCKED = 'BL', 'Blocked'
    DISCHARGE = 'DI', 'Discharge'
