# Copyright (c) 2022, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from helpdesk.utils import extract_mentions
from dontmanage.utils import get_fullname


class HDTicketComment(Document):
	def on_change(self):
		mentions = extract_mentions(self.content)

		for mention in mentions:
			values = dontmanage._dict(
				from_user=self.commented_by,
				to_user=mention.email,
				ticket=self.reference_ticket,
				comment=self.name,
			)

			if dontmanage.db.exists("HD Notification", values):
				continue

			notification = dontmanage.get_doc(doctype="HD Notification")
			notification.message = (
				f"{get_fullname(self.owner)} mentioned you in Ticket #{self.reference_ticket}",
			)
			notification.update(values)
			notification.insert(ignore_permissions=True)

	def after_insert(self):
		dontmanage.publish_realtime(
			"helpdesk:new-ticket-comment", {"ticket_id": self.reference_ticket}
		)
