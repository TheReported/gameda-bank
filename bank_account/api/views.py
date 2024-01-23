from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from bank_account.api.serializers import BankAccountSerializer
from bank_account.models import BankAccount


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)
