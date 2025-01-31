from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
import random
import string
from rest_framework import status



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

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            repeated_password = serializer.validated_data['repeated_password']
            user_type = serializer.validated_data.get('type', 'customer')  

            if password != repeated_password:
                return Response({"repeated_password": ["Die Passwörter stimmen nicht überein."]}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, email=email, user_type=user_type)
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
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