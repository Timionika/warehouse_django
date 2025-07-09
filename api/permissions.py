from rest_framework import permissions


class IsProvider(permissions.BasePermission):
    message = "Только поставщики могут поставлять товар."

    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'provider'


class IsConsumer(permissions.BasePermission):
    message = "Только потребители могут забирать товар."

    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'consumer'
    
class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser