from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )


class AdminUserOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (obj.author == request.user) 
            or request.user.is_staff
        )