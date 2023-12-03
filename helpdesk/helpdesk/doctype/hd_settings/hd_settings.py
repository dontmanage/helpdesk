# -*- coding: utf-8 -*-
# Copyright (c) 2015, DontManage and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from dontmanage.model.naming import append_number_if_name_exists
from dontmanage.model.document import Document
import dontmanage
from dontmanage.realtime import get_website_room


class HDSettings(Document):
	def get_base_support_rotation(self):
		"""Returns the base support rotation rule if it exists, else creats once and returns it"""

		if not self.base_support_rotation:
			self.create_base_support_rotation()

		return self.base_support_rotation

	def create_base_support_rotation(self):
		"""Creates the base support rotation rule, and set it to dontmanage desk settings"""

		rule_doc = dontmanage.new_doc("Assignment Rule")
		rule_doc.name = append_number_if_name_exists(
			"Assignment Rule", "Support Rotation"
		)
		rule_doc.document_type = "HD Ticket"
		rule_doc.assign_condition = "status == 'Open'"
		rule_doc.priority = 0
		rule_doc.disabled = True  # Disable the rule by default, when agents are added to the group, the rule will be enabled

		for day in [
			"Monday",
			"Tuesday",
			"Wednesday",
			"Thursday",
			"Friday",
			"Saturday",
			"Sunday",
		]:
			day_doc = dontmanage.get_doc({"doctype": "Assignment Rule Day", "day": day})
			rule_doc.append("assignment_days", day_doc)

		rule_doc.save(ignore_permissions=True)
		self.base_support_rotation = rule_doc.name
		self.save(ignore_permissions=True)

		return

	def on_update(self):
		event = "helpdesk:settings-updated"
		room = get_website_room()

		dontmanage.publish_realtime(event, room=room, after_commit=True)
