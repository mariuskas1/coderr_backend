from rest_framework import serializers
from coderr_app.models import Offer, Details



class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    details = DetailsSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])  # Extract details list
        offer = Offer.objects.create(**validated_data)  # Create Offer

        # Create related Details entries
        for detail in details_data:
            Details.objects.create(offer=offer, **detail)

        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        # Update Offer fields
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()  # Remove old details
            for detail_data in details_data:
                Details.objects.create(offer=instance, **detail_data)  # Add new details

        return instance