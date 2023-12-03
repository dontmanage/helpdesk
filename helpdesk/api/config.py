import dontmanage


@dontmanage.whitelist(allow_guest=True)
def get_config():
	fields = [
		"brand_logo",
		"prefer_knowledge_base",
		"setup_complete",
		"skip_email_workflow",
	]
	res = dontmanage.get_value(doctype="HD Settings", fieldname=fields, as_dict=True)
	return res
