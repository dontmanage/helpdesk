import dontmanage

from helpdesk.utils import extract_mentions


class HasMentions:
	def notify_mentions(self):
		"""
		Extract mentions from `mentions_field`, and notify.
		`mentions_field` must have `HTML` content.
		"""
		mentions_field = getattr(self, "mentions_field", None)
		if not mentions_field:
			return
		mentions = extract_mentions(self.get(mentions_field))
		for mention in mentions:
			values = dontmanage._dict(
				doctype="HD Notification",
				user_from=self.owner,
				user_to=mention.email,
				notification_type="Mention",
			)
			# Why mention oneself?
			if values.user_from == values.user_to:
				continue
			# Only comment (in tickets) has mentions as of now
			if self.doctype == "HD Ticket Comment":
				values.reference_comment = self.name
				values.reference_ticket = self.reference_ticket
			if dontmanage.db.exists("HD Notification", values):
				return
			dontmanage.get_doc(values).insert()
