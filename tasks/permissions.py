from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAssignee(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return obj.owner == user or user in obj.assignees.all()
        return obj.owner == user