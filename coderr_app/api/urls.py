from django.urls import path, include
from .views import OfferViewset
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'offers', OfferViewset)


urlpatterns = [
    path('', include(router.urls))
]
