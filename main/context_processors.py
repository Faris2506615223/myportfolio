from main.access import is_editor


def access_roles(request):
    """Expose the current portfolio role consistently to every template."""
    user = request.user
    editor_status = not user.is_superuser and is_editor(user)

    if not user.is_authenticated:
        role_label = "Pengunjung"
    elif user.is_superuser:
        role_label = "Pemilik"
    elif editor_status:
        role_label = "Editor"
    else:
        role_label = "Pengguna"

    return {
        "is_editor": editor_status,
        "user_role": role_label,
    }
