from rest_framework import serializers
from coderr_app.models import Offer, Details



class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    details = DetailsSerializer(many = False, required = False)

    class Meta:
        model = Offer
        fields = '__all__'
