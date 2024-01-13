from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Authenticated users only can see list view
        # TODO: in development
        # return True
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # return True

        # Read permissions are allowed to any request so we'll always
        # allow GET, HEAD, or OPTIONS requests
        # return False
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of a post
        return obj.entry.group_id_id != request.user.student.group_id_id


class IsVoter(permissions.BasePermission):
    """
    has list permission if authenticated; has retrieval permission if is the voter of the vote
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.voter == request.user.student


class IsStaff(permissions.BasePermission):
    """
    has permission only when is staff
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False


class ReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
