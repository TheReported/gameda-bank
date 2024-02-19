from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from transaction.api.serializers import TransactionSerializer
from transaction.models import Transaction


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    http_method_names = ['get']

    def get_queryset(self):
        transactions = []
        for account in self.request.user.accounts.all():
            movement = Transaction.objects.filter(Q(sender=account.code) | Q(cac=account.code))
            transactions.extend(movement)
        return transactions
