from django.urls import path, include
from .views import OfferViewset, DetailsViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'offers', OfferViewset)
router.register(r'details', DetailsViewSet)  


urlpatterns = [
    path('', include(router.urls))
]
