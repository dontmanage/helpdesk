import dontmanage


def has_app_permission():
    """Check if the user has permission to access the app."""
    if dontmanage.session.user == "Administrator":
        return True

    roles = dontmanage.get_roles()
    helpdesk_roles = ["Agent"]
    if any(role in roles for role in helpdesk_roles):
        return True

    return False
