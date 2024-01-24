from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from bank_account.utils import MovementKind
from transaction.api.serializers import TransactionSerializer
from transaction.models import Transaction


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            account__user=self.request.user, kind=MovementKind.OUTGOING
        )
