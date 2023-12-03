# Copyright (c) 2022, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class HDTicketActivity(Document):
	pass


def log_ticket_activity(ticket, action):
	return dontmanage.get_doc(
		{"doctype": "HD Ticket Activity", "ticket": ticket, "action": action}
	).insert(ignore_permissions=True)
