from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSupeuser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsNXTAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.profile in ['administrador', 'funcionario']


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and request.user.is_staff)
        )
