from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as an admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS. 
        # If the request is one of these, allow it immediately.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # If it's a write request (POST, PUT, DELETE), 
        # check if the user exists and is a staff member.
        return bool(request.user and request.user.is_staff)