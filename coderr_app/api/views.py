from rest_framework import viewsets, generics, permissions
from coderr_app.models import Offer
from .serializers import OfferSerializer, DetailsSerializer


class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer