from datetime import datetime

import dontmanage
from dontmanage.permissions import add_permission


def before_install():
	add_support_redirect_to_tickets()


def after_install():
	add_default_categories_and_articles()
	add_default_ticket_types()
	add_default_ticket_priorities()
	add_default_sla()
	add_on_ticket_create_script()
	add_default_ticket_template()
	add_default_agent_groups()
	update_agent_role_permissions()
	add_default_assignment_rule()
	add_system_preset_filters()


def add_support_redirect_to_tickets():
	website_settings = dontmanage.get_doc("Website Settings")

	for route_redirects in website_settings.route_redirects:
		if route_redirects.source == "support":
			return

	base_route = dontmanage.get_doc(
		{
			"doctype": "Website Route Redirect",
			"source": "support",
			"target": "support/tickets",
		}
	)

	website_settings.append("route_redirects", base_route)
	website_settings.save()


def add_default_categories_and_articles():
	category = dontmanage.get_doc(
		{
			"doctype": "HD Article Category",
			"category_name": "Getting Started",
			"description": "Content for your Category",
		}
	).insert()

	dontmanage.get_doc(
		{
			"doctype": "HD Article",
			"title": "Introduction",
			"content": "Content for your Article",
			"category": category.name,
			"published": False,
		}
	).insert()


def add_default_sla():

	add_default_ticket_priorities()
	add_default_holidy_list()
	enable_track_service_level_agreement_in_support_settings()

	sla_doc = dontmanage.new_doc("HD Service Level Agreement")

	sla_doc.service_level = "Default"
	sla_doc.document_type = "HD Ticket"
	sla_doc.default_sla = 1
	sla_doc.enabled = 1

	low_priority = dontmanage.get_doc(
		{
			"doctype": "HD Service Level Priority",
			"default_priority": 0,
			"priority": "Low",
			"response_time": 60 * 60 * 24,
			"resolution_time": 60 * 60 * 72,
		}
	)

	medium_priority = dontmanage.get_doc(
		{
			"doctype": "HD Service Level Priority",
			"default_priority": 1,
			"priority": "Medium",
			"response_time": 60 * 60 * 8,
			"resolution_time": 60 * 60 * 24,
		}
	)

	high_priority = dontmanage.get_doc(
		{
			"doctype": "HD Service Level Priority",
			"default_priority": 0,
			"priority": "High",
			"response_time": 60 * 60 * 1,
			"resolution_time": 60 * 60 * 4,
		}
	)

	urgent_priority = dontmanage.get_doc(
		{
			"doctype": "HD Service Level Priority",
			"default_priority": 0,
			"priority": "Urgent",
			"response_time": 60 * 30,
			"resolution_time": 60 * 60 * 2,
		}
	)

	sla_doc.append("priorities", low_priority)
	sla_doc.append("priorities", medium_priority)
	sla_doc.append("priorities", high_priority)
	sla_doc.append("priorities", urgent_priority)

	sla_fullfilled_on_resolved = dontmanage.get_doc(
		{"doctype": "HD Service Level Agreement Fulfilled On Status", "status": "Resolved"}
	)

	sla_fullfilled_on_closed = dontmanage.get_doc(
		{"doctype": "HD Service Level Agreement Fulfilled On Status", "status": "Closed"}
	)

	sla_doc.append("sla_fulfilled_on", sla_fullfilled_on_resolved)
	sla_doc.append("sla_fulfilled_on", sla_fullfilled_on_closed)

	sla_paused_on_replied = dontmanage.get_doc(
		{"doctype": "HD Pause Service Level Agreement On Status", "status": "Replied"}
	)

	sla_doc.append("pause_sla_on", sla_paused_on_replied)

	sla_doc.holiday_list = "Default"

	for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
		service_day = dontmanage.get_doc(
			{
				"doctype": "HD Service Day",
				"workday": day,
				"start_time": "10:00:00",
				"end_time": "18:00:00",
			}
		)
		sla_doc.append("support_and_resolution", service_day)

	sla_doc.insert()


def add_default_holidy_list():
	dontmanage.get_doc(
		{
			"doctype": "HD Service Holiday List",
			"holiday_list_name": "Default",
			"from_date": datetime.strptime(f"Jan 1 {datetime.now().year}", "%b %d %Y"),
			"to_date": datetime.strptime(
				f"Jan 1 {datetime.now().year + 1}", "%b %d %Y"
			),
		}
	).insert()

	dontmanage.db.commit()


def enable_track_service_level_agreement_in_support_settings():
	support_settings = dontmanage.get_doc("HD Settings")
	support_settings.track_service_level_agreement = True
	support_settings.save()
	dontmanage.db.commit()


def add_default_ticket_template():
	if dontmanage.db.exists("HD Ticket Template", "Default"):
		return

	template = dontmanage.new_doc("HD Ticket Template")

	template.template_name = "Default"
	template.append(
		"fields",
		{
			"label": "Type",
			"fieldname": "ticket_type",
			"fieldtype": "Link",
			"options": "HD Ticket Type",
			"reqd": False,
		},
	)
	template.append(
		"fields",
		{"label": "Subject", "fieldname": "subject", "fieldtype": "Data", "reqd": True},
	)
	template.append(
		"fields",
		{
			"label": "Description",
			"fieldname": "description",
			"fieldtype": "Text Editor",
			"reqd": True,
		},
	)

	template.insert()


def add_default_ticket_types():
	ticket_types = ["Question", "Bug", "Incident"]

	for type in ticket_types:
		if not dontmanage.db.exists("HD Ticket Type", type):
			type_doc = dontmanage.new_doc("HD Ticket Type")
			type_doc.name = type
			type_doc.insert()


def add_default_ticket_priorities():
	ticket_priorities = ["Low", "Medium", "High", "Urgent"]

	for priority in ticket_priorities:
		if not dontmanage.db.exists("HD Ticket Priority", priority):
			priority_doc = dontmanage.new_doc("HD Ticket Priority")
			priority_doc.name = priority
			priority_doc.insert()


def add_default_agent_groups():
	agent_groups = ["Billing", "Product Experts"]

	for agent_group in agent_groups:
		if not dontmanage.db.exists("HD Team", agent_group):
			agent_group_doc = dontmanage.new_doc("HD Team")
			agent_group_doc.team_name = agent_group
			agent_group_doc.insert()


def add_on_ticket_create_script():
	if not dontmanage.db.exists("Server Script", "Ticket Auto Set Custom Fields"):
		script_doc = dontmanage.new_doc("Server Script")
		script_doc.name = "Ticket Auto Set Custom Fields"
		script_doc.script_type = "DocType Event"
		script_doc.module = "Helpdesk"
		script_doc.reference_doctype = "HD Ticket"
		script_doc.doctype_event = "Before Insert"
		script_doc.script = "# Do Nothing"
		script_doc.insert()


def update_agent_role_permissions():
	if dontmanage.db.exists("Role", "Agent"):
		agent_role_doc = dontmanage.get_doc("Role", "Agent")
		agent_role_doc.search_bar = True
		agent_role_doc.notifications = True
		agent_role_doc.list_sidebar = True
		agent_role_doc.bulk_actions = True
		agent_role_doc.view_switcher = True
		agent_role_doc.form_sidebar = True
		agent_role_doc.form_sidebar = True
		agent_role_doc.timeline = True
		agent_role_doc.dashboard = True
		agent_role_doc.save()

		add_permission("File", "Agent", 0)
		add_permission("Contact", "Agent", 0)
		add_permission("Email Account", "Agent", 0)


def add_default_assignment_rule():
	support_settings = dontmanage.get_doc("HD Settings")
	support_settings.create_base_support_rotation()


def add_system_preset_filters():
	preset_filters = []
	for status in ["Closed", "Resolved", "Replied", "Open"]:
		preset_filters.append(
			{
				"doctype": "HD Preset Filter",
				"title": f"My {status} Tickets",
				"reference_doctype": "HD Ticket",
				"filters": [
					{
						"label": "Assigned To",
						"fieldname": "_assign",
						"filter_type": "is",
						"value": "@me",
					},
					{
						"label": "Status",
						"fieldname": "status",
						"filter_type": "is",
						"value": status,
					},
				],
			}
		)
	preset_filters.append(
		{
			"doctype": "HD Preset Filter",
			"title": "All Tickets",
			"reference_doctype": "HD Ticket",
			"filters": [],
		}
	)
	for preset in preset_filters:
		preset_filter_doc = dontmanage.get_doc(preset)
		preset_filter_doc.insert()
