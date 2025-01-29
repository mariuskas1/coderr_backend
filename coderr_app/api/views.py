from rest_framework import viewsets, generics, permissions
from coderr_app.models import Offer, Details
from .serializers import OfferSerializer, DetailsSerializer


class DetailsViewSet(viewsets.ModelViewSet):
    queryset = Details.objects.all()
    serializer_class = DetailsSerializer

class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer