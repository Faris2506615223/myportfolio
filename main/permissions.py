from rest_framework.permissions import BasePermission, SAFE_METHODS

from main.access import is_editor


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Keep the Experience API consistent with the roles from Assignment 4."""

    message = (
        "Hanya pemilik yang dapat menambah atau menghapus experience. "
        "Perubahan hanya diizinkan untuk Editor dan pemilik."
    )

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and is_editor(request.user)
        )
