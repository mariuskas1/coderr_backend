from rest_framework import serializers
from coderr_app.models import Offer, OfferDetails
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