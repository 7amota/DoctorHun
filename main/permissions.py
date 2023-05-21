
from rest_framework.permissions import BasePermission
class IsDoctor(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.isDoctor)


class CustomPermissionsForAppointements(BasePermission):
    SAFE_METHOD = ['POST']
    def has_permission(self, request, view):
        if (request.method in self.SAFE_METHOD or request.user and request.user.is_staff):
            return True
        else:
            return False
class CheckAuthor(BasePermission):
    def has_object_permission(self, request, view , obj):
        return obj.user == request.user