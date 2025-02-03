from rest_framework import permissions



class IsBusinessOwnerOrAdmin(permissions.BasePermission):
    """
    Only business users can create offers.
    Only the owner of the offer or an admin can edit/delete it.
    """

    def has_permission(self, request, view):
        """ Global permission check (applies to list & create). """
        if request.method == 'POST':
            return (
                request.user and 
                request.user.is_authenticated and 
                hasattr(request.user, 'profile') and 
                request.user.profile.type == 'business'
            )

        return True 

    def has_object_permission(self, request, view, obj):
        """ Object-level permission check (applies to update/delete). """
        if request.method in permissions.SAFE_METHODS:
            return True  
        
        return obj.user == request.user or request.user.is_staff


class IsCustomerOrAdmin(permissions.BasePermission):
    """
    Only customers can access this resource.
    Admin users (is_staff) also have full access.
    """

    def has_permission(self, request, view):
        """ Global permission check (applies to list & create). """
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            (request.user.profile.type == 'customer' or request.user.is_staff)
        )

    def has_object_permission(self, request, view, obj):
        """ Object-level permission check (applies to update/delete). """
        return self.has_permission(request, view)


class IsReviewerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the review creator or an admin to update/delete.
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET requests for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow PATCH/DELETE only if the user is the reviewer or an admin
        return obj.reviewer == request.user or request.user.is_staff
    
    
class IsCustomerUser(permissions.BasePermission):
    """
    Only users with a customer profile can create reviews.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        if not request.user or not request.user.is_authenticated:
            return False

        # Ensure the user has a customer profile (assuming `profile_type` field)
        return getattr(request.user, 'profile_type', None) == 'customer'