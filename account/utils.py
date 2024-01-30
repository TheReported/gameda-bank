import requests
from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Status.ACTIVE)


class Status(models.TextChoices):
    ACTIVE = 'AC', 'Active'
    BLOCKED = 'BL', 'Blocked'
    DISCHARGE = 'DI', 'Discharge'


def get_info_bank(account_code):
    url = 'https://raw.githubusercontent.com/sdelquin/dsw/main/ut3/te1/notes/files/banks.json'
    response = requests.get(url)
    banks = response.json()
    account_code = int(account_code[1])
    for bank in banks:
        if bank['id'] == account_code:
            return bank
