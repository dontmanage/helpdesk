import dontmanage


@dontmanage.whitelist()
def delete_items(items, doctype):
	for item in items:
		dontmanage.delete_doc(doctype, item)
