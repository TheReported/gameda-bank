from rest_framework import viewsets

from card.api.serializers import CardSerializer
from card.models import Card


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
