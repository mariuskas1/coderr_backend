from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from coderr_app.models import Offer, OfferDetails
from .serializers import OfferSerializer, OfferDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin


class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['user', 'min_price']
    search_fields = ['title', 'description']
    ordering_fields = ['min_price']

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class OfferDetailsViewSet(viewsets.ModelViewSet):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer

