from rest_framework import permissions


# Checking this user is owner of organization or not
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.methods in permissions.SAFE_METHODS:
            return True
        return obj.registrant_user == request.user
