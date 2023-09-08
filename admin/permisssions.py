from rest_framework.permissions import BasePermission


class IsDirectorUser(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.role == 4