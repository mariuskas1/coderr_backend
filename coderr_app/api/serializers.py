from rest_framework import serializers
from coderr_app.models import Offer, OfferDetails, Order
from django.contrib.auth.models import User
from django.db.models import Min




class OfferDetailsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetails
        fields = ['id', 'url'] 

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"
    

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(source='offer_details', many=True, required=False)  
    user_details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = '__all__'

    def get_user_details(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }

    def get_min_price(self, obj):
        min_price = obj.offer_details.aggregate(min_price=Min('price'))['min_price']
        return float(min_price) if min_price is not None else 0.00

    def get_min_delivery_time(self, obj):
        min_time = obj.offer_details.aggregate(min_time=Min('delivery_time_in_days'))['min_time']
        return min_time if min_time is not None else 0
    

class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(read_only=True)
    revisions = serializers.IntegerField(read_only=True)
    delivery_time_in_days = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    features = serializers.JSONField(read_only=True)
    offer_type = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def create(self, validated_data):
        offer_detail = OfferDetails.objects.get(id=validated_data['offer_detail_id'])
        offer = offer_detail.offer

        customer_user = self.context['request'].user
        business_user = offer.user  

        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            offer_detail=offer_detail,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress'
        )
        return order
    
class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']