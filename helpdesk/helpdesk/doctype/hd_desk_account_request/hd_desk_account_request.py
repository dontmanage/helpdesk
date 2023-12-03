import dontmanage
from dontmanage.model.document import Document
from dontmanage.utils import random_string, get_url


class HDDeskAccountRequest(Document):
	def before_save(self):
		if not self.request_key:
			self.request_key = random_string(32)

		self.ip_address = dontmanage.local.request_ip

	def after_insert(self):
		self.send_verification_email()

	def send_verification_email(self):
		url = get_url(f"/helpdesk/verify/{self.request_key}")
		subject = "Verify your account"
		sender = None

		if dontmanage.db.exists(
			"Email Account", {"name": "Support", "enable_outgoing": True}
		):
			sender = dontmanage.get_doc("Email Account", "Support").email_id

		try:
			dontmanage.sendmail(
				recipients=self.email,
				sender=sender,
				subject=subject,
				template="email_verification",
				args=dict(link=url),
				now=True,
			)
		except Exception:
			dontmanage.throw(
				"Either setup up Support email account or there should be a default"
				" outgoing email account"
			)
