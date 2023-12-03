import dontmanage


def execute():
	"""
	Move feedback rating and text from `HD Ticket Feedback Option` to `HD Ticket`.
	This is sometimes better because it avoids an extra API call when fetching.
	"""
	for t in dontmanage.get_all("HD Ticket"):
		t = dontmanage.get_doc("HD Ticket", t.name)
		if not t.feedback:
			continue
		if not dontmanage.db.exists("HD Ticket Feedback Option", t.feedback):
			continue
		f = dontmanage.get_doc("HD Ticket Feedback Option", t.feedback)
		t.db_set("feedback_rating", f.rating)
		t.db_set("feedback_text", f.label)
	dontmanage.db.commit()
