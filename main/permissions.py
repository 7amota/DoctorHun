
from rest_framework.permissions import BasePermission
class IsDoctor(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.isDoctor)
