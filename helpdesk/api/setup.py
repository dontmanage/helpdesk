import dontmanage
from helpdesk.helpdesk.doctype.hd_ticket.hd_ticket import create_communication_via_contact


@dontmanage.whitelist()
def initial_agent_setup():
	support_settings_doc = dontmanage.get_doc("HD Settings", "HD Settings")
	if dontmanage.db.count("HD Agent") == 0:
		agent_added = False
		users = dontmanage.get_all(
			"User", filters={"user_type": "System User"}, order_by="creation"
		)
		for user in users:
			if user.name != "Administrator":
				agent = dontmanage.new_doc("HD Agent")
				agent.user = user.name
				agent.insert()
				agent_added = True

		if not agent_added:
			dontmanage.throw("No user found to create agent")

	support_settings_doc.initial_agent_set = True
	support_settings_doc.save()


@dontmanage.whitelist()
def create_initial_demo_ticket():
	support_settings_doc = dontmanage.get_doc("HD Settings", "HD Settings")
	if dontmanage.db.count("HD Ticket") == 0:
		agent = dontmanage.get_last_doc("HD Agent")
		if agent:
			dontmanage.get_doc(
				{
					"doctype": "Contact",
					"first_name": "Harshit",
					"last_name": "Agrawal",
					"email_ids": [{"email_id": "harshit@dontmanage.io", "is_primary": 1}],
				}
			).insert()

			new_ticket_doc = dontmanage.new_doc("HD Ticket")
			new_ticket_doc.subject = "Welcome to Helpdesk"
			new_ticket_doc.description = """
			<p>Hi 👋🏻</p>
			<p><br></p>
			<p>I'm glad you decided to try Helpdesk! We're working hard to build a better way for teams to communicate and serve customers well. I'm excited to get started.</p>
			<p><br></p>
			<p>You can get started right away by setting up a support email. This will help you see what your support will look like with DontManage Helpdesk!</p>
			<p><br></p>
			<p>Best,</p>
			<p>Harshit</p>
			<p>Helpdesk | DontManage.</p>
			"""
			new_ticket_doc.raised_by = "harshit@dontmanage.io"
			new_ticket_doc.contact = "Harshit Agrawal"
			new_ticket_doc.via_customer_portal = True
			new_ticket_doc.insert()

			create_communication_via_contact(new_ticket_doc.name, new_ticket_doc.description)
	support_settings_doc.initial_demo_ticket_created = True
	support_settings_doc.save()
	return
