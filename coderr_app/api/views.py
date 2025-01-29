from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from coderr_app.models import Offer, Details
from .serializers import OfferSerializer, DetailsSerializer


class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['user', 'min_price']
    search_fields = ['title', 'description']
    ordering_fields = ['min_price']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class DetailsViewSet(viewsets.ModelViewSet):
    queryset = Details.objects.all()
    serializer_class = DetailsSerializer

