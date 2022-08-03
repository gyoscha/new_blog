from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyAuthorEditNote(BasePermission):
    """ Только автор поста может его изменить """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.user
