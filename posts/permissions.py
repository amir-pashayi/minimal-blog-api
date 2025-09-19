from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            getattr(obj, "user_id", None) == getattr(request.user, "id", None)
            or getattr(request.user, "is_staff", False)
        )
