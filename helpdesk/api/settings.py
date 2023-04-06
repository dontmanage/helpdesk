import dontmanage


@dontmanage.whitelist()
def update_helpdesk_name(name):
	doc = dontmanage.get_doc("HD Settings")
	doc.helpdesk_name = name
	doc.save(ignore_permissions=True)

	return doc.helpdesk_name


@dontmanage.whitelist()
def skip_helpdesk_name_setup():
	doc = dontmanage.get_doc("HD Settings")
	doc.initial_helpdesk_name_setup_skipped = True
	doc.save(ignore_permissions=True)

	return doc
