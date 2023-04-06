import dontmanage


def pull_support_emails():
	email_accounts = dontmanage.get_all(
		"Email Account",
		filters=[["IMAP Folder", "append_to", "=", "HD Ticket"]],
		fields=["name"],
	)
	for account in email_accounts:
		email_account = dontmanage.get_doc("Email Account", account["name"])

		if email_account.enable_incoming:
			email_account.receive()


def on_assignment_rule_trash(doc, event):
	if not dontmanage.get_all(
		"Assignment Rule", filters={"document_type": "HD Ticket", "name": ["!=", doc.name]}
	):
		dontmanage.throw("There should atleast be 1 assignment rule for ticket")
