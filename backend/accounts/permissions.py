from rest_framework.permissions import BasePermission


class IsAdminUserCustom(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "staff"


class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "manager"