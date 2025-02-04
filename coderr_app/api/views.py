from rest_framework import viewsets, filters, status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from coderr_app.models import Offer, OfferDetails, Order, Review
from .serializers import OfferSerializer, OfferDetailsSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderStatusSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessOwnerOrAdmin, IsCustomerOrAdmin, IsCustomerUser, IsReviewerOrAdmin
from .pagination import CustomPageNumberPagination  
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Avg




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
    

class BaseInfoViewset(APIView):
    def get(self, request):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        average_rating = round(average_rating, 1) if average_rating is not None else 0.0
        business_profile_count = User.objects.filter(type = 'business').count()
        offer_count = Offer.objects.count()

        return Response({
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        })


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer'] 
    ordering_fields = ['rating', 'created_at'] 

    def get_permissions(self):
        """Apply different permissions based on the action."""
        if self.action in ['create']:
            return [IsCustomerUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsReviewerOrAdmin()]
        return [permissions.IsAuthenticated()]  # Default: Any authenticated user can read reviews

    def partial_update(self, request, *args, **kwargs):
        """Restrict editable fields to only 'rating' and 'description'."""
        allowed_fields = {'rating', 'description'}
        request.data = {key: value for key, value in request.data.items() if key in allowed_fields}
        return super().partial_update(request, *args, **kwargs)
    
    
