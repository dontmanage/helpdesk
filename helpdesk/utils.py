import re
from typing import List

import dontmanage
from bs4 import BeautifulSoup
from dontmanage.model.document import Document
from dontmanage.realtime import get_website_room
from dontmanage.utils.safe_exec import get_safe_globals
from dontmanage.utils.telemetry import capture as _capture
from pypika import Criterion


def check_permissions(doctype, parent):
    user = dontmanage.session.user

    permissions = ("select", "read")
    has_select_permission, has_read_permission = [
        dontmanage.has_permission(doctype, perm, user=user, parent_doctype=parent)
        for perm in permissions
    ]

    if not has_select_permission and not has_read_permission:
        dontmanage.throw(f"Insufficient Permission for {doctype}", dontmanage.PermissionError)


def is_admin(user: str = None) -> bool:
    """
    Check whether `user` is an admin

    :param user: User to check against, defaults to current user
    :return: Whether `user` is an admin
    """
    user = user or dontmanage.session.user
    return user == "Administrator"


def is_agent(user: str = None) -> bool:
    """
    Check whether `user` is an agent

    :param user: User to check against, defaults to current user
    :return: Whether `user` is an agent
    """
    user = user or dontmanage.session.user
    return (
        is_admin()
        or "Agent" in dontmanage.get_roles(user)
        or bool(dontmanage.db.exists("HD Agent", {"name": user}))
    )


def publish_event(event: str, data: dict, user: str = None):
    """
    Publish `event` to a room with `data`

    :param event: Event name. Example: "refetch_resource"
    :param data: Data to be sent with the event
    :param user: User to send the event to, defaults to current user
    """
    room = get_website_room()
    user = user or dontmanage.session.user
    dontmanage.publish_realtime(
        event, message=data, room=room, after_commit=True, user=user
    )


def refetch_resource(key: str | List[str], user=None):
    event = "refetch_resource"
    data = {"cache_key": key}
    publish_event(event, data, user=user)


def capture_event(event: str):
    return _capture(event, "helpdesk")


@dontmanage.whitelist()
def get_customer(contact: str) -> tuple[str]:
    """
    Get `Customer` from `Contact`

    :param contact: Contact which belongs to a customer
    :return: Customer `name` if available
    """
    QBDynamicLink = dontmanage.qb.DocType("Dynamic Link")
    QBContact = dontmanage.qb.DocType("Contact")
    conditions = [QBDynamicLink.parent == contact, QBContact.email_id == contact]
    return [
        i[0]
        for i in (
            dontmanage.qb.from_(QBDynamicLink)
            .select(QBDynamicLink.link_name)
            .where(QBDynamicLink.parentfield == "links")
            .where(QBDynamicLink.parenttype == "Contact")
            .where(QBDynamicLink.link_doctype == "HD Customer")
            .join(QBContact)
            .on(QBDynamicLink.parent == QBContact.name)
            .where(Criterion.any(conditions))
            .run()
        )
    ]


def extract_mentions(html):
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    mentions = []
    for d in soup.find_all("span", attrs={"data-type": "mention"}):
        mentions.append(
            dontmanage._dict(full_name=d.get("data-label"), email=d.get("data-id"))
        )
    return mentions


def alphanumeric_to_int(s: str) -> int | None:
    """
    Get int from alphanumeric string, using regex
    String example: "foo-123" -> 123


    :param s: Alphanumeric string to be searched for
    :return: Integer if a number is found
    """
    s = re.search(r"\d+", s)

    if not s:
        return

    return int(s.group(0))


def get_context(d: Document) -> dict:
    """
    Get safe context for `safe_eval`

    :param doc: `Document` to add in context
    :return: Context with `doc` and safe variables
    """
    utils = get_safe_globals().get("dontmanage").get("utils")
    return {
        "doc": d.as_dict(),
        "dontmanage": dontmanage._dict(utils=utils),
    }
