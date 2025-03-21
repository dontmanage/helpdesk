import dontmanage


@dontmanage.whitelist()
def clear(user: str = None, ticket: str | int = None, comment: str = None):
    """
    Mark notifications as read. No arguments will clear all notifications for `user`.

    :param user: User to clear notifications for. Defaults to current `user`
    :param ticket: Ticket to clear notifications for
    :param comment: Comment to clear notifications for
    """
    user = user or dontmanage.session.user
    filters = {"user_to": user, "read": False}
    if ticket:
        filters["reference_ticket"] = ticket
    if comment:
        filters["reference_comment"] = comment
    for notification in dontmanage.get_all(
        "HD Notification", filters=filters, pluck="name"
    ):
        dontmanage.db.set_value("HD Notification", notification, "read", 1)
