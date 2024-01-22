from rest_framework import viewsets

from transaction.api.serializers import TransactionSerializer
from transaction.models import Transaction


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
