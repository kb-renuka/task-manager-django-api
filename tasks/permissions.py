from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Only the owner of a Task/Category can view, edit, or delete it."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
