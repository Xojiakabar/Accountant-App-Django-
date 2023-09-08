from rest_framework.permissions import BasePermission


class IsClient(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return request.user.role == 1
        return False


class IsAccountant(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return request.user.role == 2
        return False
