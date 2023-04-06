import dontmanage


@dontmanage.whitelist()
def get_canned_response(title=None):
	if title == None:
		response_list = dontmanage.db.get_list(
			"HD Canned Response", fields=["name", "title", "message"]
		)
	else:
		response_list = dontmanage.db.get_list(
			"HD Canned Response",
			fields=["name", "title", "message"],
			filters={"title": ["like", "%{}%".format(title)]},
		)

	return response_list
