from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        basic = bool(request.user and request.user.is_authenticated)
        if request.user.is_writer:
            return bool(
                basic
                and request.user.writerprofile.id
                == request.parser_context["kwargs"]["pk"]
            )

        elif request.user.is_reader:
            return bool(
                basic
                and request.user.readerprofile.id
                == request.parser_context["kwargs"]["pk"]
            )
        return False
