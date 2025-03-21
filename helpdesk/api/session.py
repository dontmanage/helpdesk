import dontmanage
from dontmanage import _

from helpdesk.utils import is_agent


@dontmanage.whitelist()
def get_users():
    if not is_agent():
        dontmanage.throw(_("Access denied"), exc=dontmanage.PermissionError)

    if dontmanage.session.user == "Guest":
        dontmanage.throw(dontmanage._("Authentication failed"), exc=dontmanage.AuthenticationError)

    users = dontmanage.qb.get_query(
        "User",
        fields=["name", "email", "enabled", "user_image", "full_name", "user_type"],
        order_by="full_name asc",
        distinct=True,
    ).run(as_dict=1)

    for user in users:
        if dontmanage.session.user == user.name:
            user.session_user = True

    return users
