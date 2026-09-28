from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


EDITOR_GROUP_NAME = "Editor"


def is_editor(user):
    """Return whether an authenticated user belongs to the Editor group."""
    return (
        user.is_authenticated
        and user.groups.filter(name=EDITOR_GROUP_NAME).exists()
    )


def _role_required(predicate):
    """Require login first, then return HTTP 403 when a role check fails."""

    def decorator(view_func):
        @login_required(login_url="/login/")
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not predicate(request.user):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


portfolio_owner_required = _role_required(lambda user: user.is_superuser)
experience_editor_required = _role_required(
    lambda user: user.is_superuser or is_editor(user)
)
