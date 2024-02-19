from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from bank_account.api.serializers import BankAccountSerializer
from bank_account.models import BankAccount


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    http_method_names = ['get']

    def get_queryset(self):
        return BankAccount.active.filter(user=self.request.user)
