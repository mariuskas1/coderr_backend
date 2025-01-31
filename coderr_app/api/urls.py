from django.urls import path, include
from .views import OfferViewset, OfferDetailsViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'offers', OfferViewset)
router.register(r'offerdetails', OfferDetailsViewSet)  


urlpatterns = [
    path('', include(router.urls))
]
