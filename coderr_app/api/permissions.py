from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Only authenticated users who are the owner of the offer or an admin can edit/delete.
    Only providers (e.g., authenticated users) can create offers.
    """

    def has_permission(self, request, view):
        """ Global permission check (applies to list & create). """
        if request.method == 'POST':
            return request.user and request.user.is_authenticated  
        
        return True  

    def has_object_permission(self, request, view, obj):
        """ Object-level permission check (applies to update/delete). """
        if request.method in permissions.SAFE_METHODS:
            return True  
        
        return obj.user == request.user or request.user.is_staff
