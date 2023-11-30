from rest_framework import permissions


class IsReader(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_reader
        )


class IsSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.readerprofile.id == request.data["subscribing_user"]
