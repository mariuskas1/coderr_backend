from django.urls import path
from .views import RegistrationView, CustomLoginView, GuestLoginView, UserProfileDetailView, BusinessUserListView, CustomerUserListView

urlpatterns = [
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),
    path('profiles/business/', BusinessUserListView.as_view(), name='business-user-list'),
    path('profiles/customer/', CustomerUserListView.as_view(), name='customer-user-list'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
]