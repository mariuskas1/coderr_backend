from rest_framework import serializers
from coderr_app.models import Offer, Details
from django.contrib.auth.models import User



class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    details = DetailsSerializer(many=True, required=False)  
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = '__all__'

    def get_user_details(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])  
        offer = Offer.objects.create(**validated_data)

        for detail in details_data:
            Details.objects.create(offer=offer, **detail)

        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                Details.objects.create(offer=instance, **detail_data)

        return instance