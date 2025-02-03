from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from coderr_app.models import Offer, OfferDetails, Order
from .serializers import OfferSerializer, OfferDetailsSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderStatusSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessOwnerOrAdmin, IsCustomerOrAdmin
from .pagination import CustomPageNumberPagination  
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User



class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticated, IsBusinessOwnerOrAdmin]
    pagination_class = CustomPageNumberPagination

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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsCustomerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return Order.objects.filter(customer_user=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action == 'create':
            return CreateOrderSerializer
        if self.action == 'partial_update':  
            return UpdateOrderStatusSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        """Automatically assign the authenticated user as the customer."""
        serializer.save(customer_user=self.request.user)




class OrderCountView(APIView):
    def get(self, request, business_user_id): 
        business_user = get_object_or_404(User, id=business_user_id)
        order_count = Order.objects.filter(business_user=business_user, status='in_progress').count()
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)
    

class CompletedOrderCountView(APIView):
    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, id=business_user_id)
        completed_order_count = Order.objects.filter(business_user=business_user, status='completed').count()
        return Response({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)