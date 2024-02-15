from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from card.api.serializers import CardSerializer
from card.models import Card


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    http_method_names = ['get']

    def get_queryset(self):
        return Card.objects.filter(bank_account__user=self.request.user)
