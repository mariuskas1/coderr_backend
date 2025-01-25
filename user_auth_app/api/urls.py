from django.urls import path
from .views import UserProfileList, UserProfileDetail, RegistrationView, CustomLoginView, GuestLoginView

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('guest-login/', GuestLoginView.as_view(), name='guest-login')
]