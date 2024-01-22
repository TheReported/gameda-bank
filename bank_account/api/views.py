from rest_framework import viewsets

from bank_account.api.serializers import BankAccountSerializer
from bank_account.models import BankAccount


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
