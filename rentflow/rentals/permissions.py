from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пермишен, позволяющий только владельцу объекта редактировать/удалять его.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user