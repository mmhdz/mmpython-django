from rest_framework.permissions import BasePermission, SAFE_METHODS
from http import HTTPMethod
from .models import UserRole

class IsAdminOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.role == UserRole.ADMIN or obj.user == request.user



class IsOwner(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
        

    def has_object_permission(self, request, view, obj):
        if request.method == HTTPMethod.PUT:
            return request.user.role == UserRole.ADMIN or obj.user == request.user
        return obj.user == request.user
    

