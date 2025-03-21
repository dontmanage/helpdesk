import dontmanage

from helpdesk.utils import is_agent as _is_agent


@dontmanage.whitelist()
def get_user():
    current_user = dontmanage.session.user
    filters = {"name": current_user}
    fields = [
        "first_name",
        "full_name",
        "name",
        "user_image",
        "username",
        "time_zone",
    ]
    user = dontmanage.get_value(
        doctype="User",
        filters=filters,
        fieldname=fields,
        as_dict=True,
    )

    is_agent = _is_agent()
    is_admin = ("System Manager" or "Admistrator") in dontmanage.get_roles(current_user)
    has_desk_access = is_agent or is_admin
    user_image = user.user_image
    user_first_name = user.first_name
    user_name = user.full_name
    user_id = user.name
    username = user.username
    is_manager = ("Agent Manager") in dontmanage.get_roles(current_user)

    return {
        "has_desk_access": has_desk_access,
        "is_admin": is_admin,
        "is_agent": is_agent,
        "user_id": user_id,
        "is_manager": is_manager,
        "user_image": user_image,
        "user_first_name": user_first_name,
        "user_name": user_name,
        "username": username,
        "time_zone": user.time_zone,
    }


@dontmanage.whitelist(allow_guest=True)
def oauth_providers():
    from dontmanage.utils.html_utils import get_icon_html
    from dontmanage.utils.oauth import get_oauth2_authorize_url, get_oauth_keys
    from dontmanage.utils.password import get_decrypted_password

    out = []
    providers = dontmanage.get_all(
        "Social Login Key",
        filters={"enable_social_login": 1},
        fields=["name", "client_id", "base_url", "provider_name", "icon"],
        order_by="name",
    )

    for provider in providers:
        client_secret = get_decrypted_password(
            "Social Login Key", provider.name, "client_secret"
        )
        if not client_secret:
            continue

        icon = None
        if provider.icon:
            if provider.provider_name == "Custom":
                icon = get_icon_html(provider.icon, small=True)
            else:
                icon = f"<img src='{provider.icon}' alt={provider.provider_name}>"

        if provider.client_id and provider.base_url and get_oauth_keys(provider.name):
            out.append(
                {
                    "name": provider.name,
                    "provider_name": provider.provider_name,
                    "auth_url": get_oauth2_authorize_url(provider.name, "/helpdesk"),
                    "icon": icon,
                }
            )

    return out
