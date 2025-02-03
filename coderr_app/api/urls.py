from django.urls import path, include
from .views import OfferViewset, OfferDetailsViewSet, OrderViewSet, OrderCountView
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'offers', OfferViewset)
router.register(r'offerdetails', OfferDetailsViewSet)  
router.register(r'oders', OrderViewSet)  


urlpatterns = [
    path('', include(router.urls)),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count')
]
