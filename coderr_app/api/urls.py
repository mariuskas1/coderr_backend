from django.urls import path, include
from .views import OfferViewset, OfferDetailsViewSet, OrderViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'offers', OfferViewset)
router.register(r'offerdetails', OfferDetailsViewSet)  
router.register(r'oders', OrderViewSet)  


urlpatterns = [
    path('', include(router.urls))
]
