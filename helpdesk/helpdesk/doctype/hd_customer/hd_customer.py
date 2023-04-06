# Copyright (c) 2022, DontManage Technologies and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class HDCustomer(Document):
	pass


def get_contact_count(doc, event):
	if len(doc.links) == 0:
		return

	contact_count = dontmanage.db.count(
		"Dynamic Link",
		{
			"link_doctype": "HD Customer",
			"link_name": doc.links[0].link_name,
			"parenttype": "Contact",
		},
	)
	customer = dontmanage.get_doc("HD Customer", doc.links[0].link_name)
	customer.contact_count = contact_count

	customer.save()


def get_ticket_count(doc, event):
	if not doc.customer:
		return

	ticket_count = dontmanage.db.count("HD Ticket", {"customer": doc.customer})
	customer = dontmanage.get_doc("HD Customer", doc.customer)
	customer.ticket_count = ticket_count

	customer.save()
