from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'name']


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    repeated_password = serializers.CharField(write_only=True, required=True, min_length=6)
    type = serializers.ChoiceField(choices=UserProfile.USER_TYPES, default='customer')  

    def validate_username(self, value):
        """ Ensure the username is unique """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Dieser Benutzername ist bereits vergeben.")
        return value

    def validate_email(self, value):
        """ Ensure the email is unique """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Diese E-Mail-Adresse wird bereits verwendet.")
        return value

    def validate(self, data):
        """ Ensure passwords match """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"repeated_password": "Die Passwörter stimmen nicht überein."})
        return data
       
