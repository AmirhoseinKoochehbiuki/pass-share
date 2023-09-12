from rest_framework import permissions
from pass_box.models import *


class PassOwnerPermission_Read(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return False


class PassOwnerPermission_Create(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return False


class PassOwnerPermission_Update(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH'] and request.data:
            """user should own the Pass To update"""
            owner_id = PassBox.objects.get(
                id=int(request.parser_context['kwargs']['pk'])).owner_id
            if owner_id == request.user.id:
                return True
        if request.method in ['PUT', 'PATCH'] and not request.data:
            return True
        return False


class PassOwnerPermission_Delete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE' and request._request.method == 'DELETE':
            """user should own the pass to delete"""
            owner_id = PassBox.objects.get(id=view.kwargs['pk']).owner_id
            if owner_id == request.user.id:
                return True
        if request.method == 'DELETE' and request._request.method == 'GET':
            return True
        return False


class SharePassOwnerPermission_Read(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return False


class SharePassOwnerPermission_Create(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.data:
            """user should own the pass to Share"""
            if PassBox.objects.get(id=int(request.data['pass_code'])).owner_id == request.user.id:
                return True
        if request.method == 'POST' and not request.data:
            return True
        return False


class SharePassOwnerPermission_Update(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH'] and request.data:
            """user should own the pass to update Share"""
            if PassBox.objects.get(id=int(request.data['pass_code'])).owner_id == request.user.id:
                return True
        if request.method in ['PUT', 'PATCH'] and not request.data:
            return True
        return False


class SharePassOwnerPermission_Delete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE' and request._request.method == 'DELETE':
            """user should own the pass to delete Share"""
            pass_code_id = ShareList.objects.get(
                id=int(view.kwargs['pk'])).pass_code_id
            if PassBox.objects.get(id=pass_code_id).owner_id == request.user.id:
                return True
        if request.method == 'DELETE' and request._request.method == 'GET':
            return True
        return False
