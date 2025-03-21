import dontmanage
from dontmanage import _
from dontmanage.utils.telemetry import capture

no_cache = 1


def get_context(context):
    context.csrf_token = dontmanage.sessions.get_csrf_token()
    context.site_name = dontmanage.local.site
    # website favicon
    context.favicon = get_favicon()
    dontmanage.db.commit()

    # telemetry
    if dontmanage.session.user != "Guest":
        capture("active_site", "helpdesk")
    return context


@dontmanage.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
    if not dontmanage.conf.developer_mode:
        dontmanage.throw(_("This method is only meant for developer mode"))
    return get_boot()


def get_boot():
    return dontmanage._dict(
        {
            "default_route": get_default_route(),
            "site_name": dontmanage.local.site,
            "read_only_mode": dontmanage.flags.read_only,
            "csrf_token": dontmanage.sessions.get_csrf_token(),
            "favicon": get_favicon(),
        }
    )


def get_default_route():
    return "/helpdesk"


def get_favicon():
    return (
        dontmanage.db.get_single_value("Website Settings", "favicon")
        or "/assets/helpdesk/desk/favicon.svg"
    )
