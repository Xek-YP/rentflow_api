from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменение только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsBookingParticipant(permissions.BasePermission):
    """
    Разрешает доступ только участникам бронирования (гость или владелец жилья).
    """
    def has_object_permission(self, request, view, obj):
        return obj.guest == request.user or obj.rental_listing.owner == request.user