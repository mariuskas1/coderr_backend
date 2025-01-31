from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
import random
import string



class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Users can only view/update their own profile.
        Admins can view/update any profile.
        """
        user = self.request.user
        if user.is_staff:  # Admins can access all profiles
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)  # Regular users can only access their own profile



class BusinessUserListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return UserProfile.objects.filter(user_type='business')


class CustomerUserListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return UserProfile.objects.filter(user_type='customer')



class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data= {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'name': saved_account.first_name
            }
        else:
            data=serializer.errors
        
        return Response(data)
    


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'name': user.first_name
            }
        else:
            data = serializer.errors
        
        return Response(data)
    
    
class GuestLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        random_username = "guest_" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        guest_user = User.objects.create_user(username=random_username)
        
        token, _ = Token.objects.get_or_create(user=guest_user)

        return Response({
            "token": token.key,
            "username": guest_user.username,
            "is_guest": True
        })