from rest_framework import permissions


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

