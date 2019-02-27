from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_condition import And, Or

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS  

class MyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.method in SAFE_METHODS)

CustomPermission = And(Or(IsReadOnly,IsAdmin), IsAuthenticated)
