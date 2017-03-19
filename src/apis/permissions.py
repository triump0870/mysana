from rest_framework import permissions


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff():
            return True
        return obj.user == request.userz
