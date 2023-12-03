import dontmanage
from dontmanage import _

from helpdesk.utils import is_agent


@dontmanage.whitelist(allow_guest=True)
def get_article(name: str):
	article = dontmanage.get_doc("HD Article", name).as_dict()

	if not is_agent() and article["status"] != "Published":
		dontmanage.throw(_("Access denied"), dontmanage.PermissionError)

	author = dontmanage.get_cached_doc("User", article["author"])
	sub_category = dontmanage.get_cached_doc("HD Article Category", article["category"])
	category = dontmanage.get_cached_doc(
		"HD Article Category", sub_category.parent_category
	)

	return {
		**article,
		"author": author,
		"category": category,
		"sub_category": sub_category,
	}
