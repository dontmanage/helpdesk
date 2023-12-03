import dontmanage


@dontmanage.whitelist()
def get_list_public():
	fields = ["name", "category_name", "icon"]
	categories = dontmanage.get_list(
		"HD Article Category", fields=fields, filters={"parent_category": ""}
	)
	res = []

	for category in categories:
		sub_categories = dontmanage.get_list(
			"HD Article Category",
			filters={"parent_category": category.name},
			fields=fields,
		)
		category.sub_categories = sub_categories
		if len(sub_categories):
			res.append(category)

	return res
