from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from coderr_app.models import Offer, OfferDetails
from .serializers import OfferSerializer, OfferDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessOwnerOrAdmin
from rest_framework.pagination import PageNumberPagination



class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticated, IsBusinessOwnerOrAdmin]

    filterset_fields = {
        'user': ['exact'], 
        'offer_details__price': ['gte'],  
        'offer_details__delivery_time_in_days': ['lte'],  
    }
    search_fields = ['title', 'description']
    ordering_fields = ['min_price']


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class OfferDetailsViewSet(viewsets.ModelViewSet):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer

